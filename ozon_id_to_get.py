# SPDX-License-Identifier: BSD-3-Clause
#
# Copyright (c) 2026, Diana McLOVIN / Raxanarch
#
# This file is part of ojob-warehouse-id-searcher.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the BSD 3-Clause License.
# See the LICENSE file for details.

# -*- coding: utf-8 -*-
from burp import IBurpExtender, IHttpListener
import re


class BurpExtender(IBurpExtender, IHttpListener):

    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()

        callbacks.setExtensionName("Ozon Warehouse ID -> Name (by-filter rewrite)")
        callbacks.registerHttpListener(self)

        self._search_re = re.compile(r'"search"\s*:\s*"(\d{10,})"')
        self._name_re = re.compile(r'"name"\s*:\s*"((?:[^"\\]|\\.)*)"')

        print("[+] Extension loaded")

    def _safe_print(self, msg):
        try:
            print(msg)
        except Exception:
            try:
                print(repr(msg))
            except Exception:
                print("[!] (unprintable debug line)")

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if not messageIsRequest:
            return

        http_service = messageInfo.getHttpService()
        if http_service is None or http_service.getHost() != "ojob.ozon.ru":
            return

        request = messageInfo.getRequest()
        analyzed = self.helpers.analyzeRequest(messageInfo)

        method = analyzed.getMethod()
        path = analyzed.getUrl().getPath()

        if method != "POST" or path != "/v2/object/by-filter":
            return

        self._safe_print("[+] Found POST /v2/object/by-filter")

        body_offset = analyzed.getBodyOffset()
        body_text = self.helpers.bytesToString(request[body_offset:])

        match = self._search_re.search(body_text)
        if not match:
            self._safe_print("[-] Numeric warehouse ID not found, skip")
            return

        warehouse_id = match.group(1)
        self._safe_print("[+] Warehouse ID: " + warehouse_id)

        headers = analyzed.getHeaders()
        original_request_line = headers[0]
        http_version = "HTTP/2" if original_request_line.rstrip().endswith("HTTP/2") else "HTTP/1.1"

        side_headers = ["GET /v2/object/%s %s" % (warehouse_id, http_version)]
        for header in headers[1:]:
            name_h = header.split(":", 1)[0].strip().lower()
            if name_h in ("content-length", "content-type", "transfer-encoding", "accept-encoding"):
                continue
            side_headers.append(header)
        side_headers.append("Accept-Encoding: identity")

        side_request = self.helpers.buildHttpMessage(side_headers, None)

        try:
            side_response_obj = self.callbacks.makeHttpRequest(http_service, side_request)
        except Exception as e:
            self._safe_print("[-] Side request failed: " + str(e))
            return

        side_response = side_response_obj.getResponse()
        if side_response is None:
            self._safe_print("[-] No response from side GET request")
            return

        resp_info = self.helpers.analyzeResponse(side_response)
        status_code = resp_info.getStatusCode()
        resp_body_offset = resp_info.getBodyOffset()
        resp_body_text = self.helpers.bytesToString(side_response[resp_body_offset:])

        self._safe_print("[DEBUG] Side response status: %d" % status_code)
        self._safe_print("[DEBUG] Side response body len: %d" % len(resp_body_text))

        if status_code != 200:
            self._safe_print("[-] Side request did not return 200, skip")
            return

        name_match = self._name_re.search(resp_body_text)
        if not name_match:
            self._safe_print("[-] Could not extract 'name' from side response")
            return

        warehouse_name = name_match.group(1)
        self._safe_print("[+] Resolved name (len=%d chars)" % len(warehouse_name))

        new_body_text = body_text.replace(
            '"search":"%s"' % warehouse_id,
            '"search":"%s"' % warehouse_name
        )

        if new_body_text == body_text:
            self._safe_print("[-] Failed to substitute name into body")
            return

        new_body_bytes = self.helpers.stringToBytes(new_body_text)

        new_headers = []
        for header in headers:
            if header.split(":", 1)[0].strip().lower() == "content-length":
                continue
            new_headers.append(header)
        new_headers.append("Content-Length: %d" % len(new_body_bytes))

        new_request = self.helpers.buildHttpMessage(new_headers, new_body_bytes)
        messageInfo.setRequest(new_request)

        self._safe_print("[+] REWRITTEN body, search length now = %d" % len(new_body_text))
