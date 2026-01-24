# 📘 Project: Gemini Journal Automation Pipeline

**Status:** ✅ Production Ready
**Date:** 2026-01-19
**Owner:** Tariq Khan

## 1. Executive Summary

This workflow automates the extraction of structured journal entries from Google Gemini and archives them as native Google Docs in a personal Knowledge Management system.

**The Challenge:** Direct API calls from the browser console (Bookmarklet) to a private n8n server are blocked by Google's strict **Content Security Policy (CSP)** and **CORS** rules.
**The Solution:** A "Bridge Architecture" that uses a client-side Javascript bookmarklet to capture content and a server-side **n8n Form Portal** to bypass browser security restrictions safely.

---

## 2. Architecture Overview

**Flow:** `User (Gemini UI)` → `Bookmarklet (Clipboard)` → `n8n Form Portal` → `Processing` → `Google Drive`

| Component     | Technology        | Responsibility                                            |
| ------------- | ----------------- | --------------------------------------------------------- |
| **Trigger**   | JS Bookmarklet    | Scrapes selected text, copies to clipboard, opens Portal. |
| **Ingest**    | n8n Form Trigger  | Hosted UI to accept text input (Bypasses CORS).           |
| **Parser**    | Javascript (Node) | Extracts `YYYY-MM-DD` date from header for file naming.   |
| **Converter** | Binary Processor  | Converts raw text string into a file object.              |
| **Storage**   | Google Drive API  | Saves file and auto-converts to editable Google Doc.      |

---

## 3. Client-Side Configuration (The "Bridge")

**Tool:** Browser Bookmarklet
**Function:** 1-Click scrape and handoff.

```javascript
javascript: (function () {
  /* 1. Get Highlighted Text from Gemini */
  const selection = window.getSelection().toString();
  if (!selection) {
    alert("⚠️ Please highlight your Journal text first!");
    return;
  }

  /* 2. Copy to Clipboard (System Bridge) */
  navigator.clipboard
    .writeText(selection)
    .then(() => {
      /* 3. Open n8n Ingest Portal */
      /* Production URL: Host-specific UUID */
      const n8nUrl =
        "https://n8n.khantastic.org/form/bfcfbb81-c125-406a-8f36-2f151fa8c1b0";
      window.open(n8nUrl, "JournalIngest", "width=600,height=800");
    })
    .catch((err) => {
      alert("❌ Clipboard Copy Failed: " + err);
    });
})();
```

---

## 4. Server-Side Configuration (n8n Workflow)

#### Node 1: Form Trigger (Ingest)

- **Type:** `n8n Form Trigger`
- **Field Name:** `body` (Text Area)
- **URL Type:** Production

#### Node 2: Date Parser (Logic)

- **Type:** `Code` (Javascript)
- **Purpose:** Extracts date from `## Journal Entry: YYYY-MM-DD` header.
- **Code Logic:**

```javascript
const regex = /## Journal Entry:\s*(\d{4}-\d{2}-\d{2})/;
const match = $json.body.match(regex);
// Fallback to today if no date found in text
const date = match ? match[1] : new Date().toISOString().split("T")[0];

return {
  json: {
    date: date,
    fileName: `Journal Entry - ${date}`,
    content: $json.body,
  },
};
```

#### Node 3: String-to-File (The Pivot)

- **Type:** `Convert to File`
- **Operation:** `Convert to Text File`
- **Configuration (Crucial):**
- **File Content:** `content` (⚠️ Input the **Field Key**, not the Expression `{{...}}`).
- **File Name:** `{{ $json.fileName }}.txt`

#### Node 4: Cloud Storage (Archive)

- **Type:** `Google Drive`
- **Operation:** `Upload`
- **Input Data:** `data` (Binary property from Node 3).
- **Options:** `Convert to Google Document` = **TRUE**.

---

## 5. Troubleshooting Log (Root Cause Analysis)

- **Issue:** `TypeError: Failed to fetch`
- **Cause:** Browser blocked request due to CORS/CSP rules on `google.com`.
- **Fix:** Switched from hidden `fetch()` webhook to user-initiated **Form Portal**.

- **Issue:** `Error: Value in "..." is not set`
- **Cause:** The "Convert to File" node received the entire text body as the _key name_ instead of the _content_.
- **Fix:** Changed "File Content" field from `{{ $json.content }}` (Value) to `content` (Key).

- **Issue:** `Binary Data Expectation`
- **Cause:** Google Drive node expects a file object, not a JSON string.
- **Fix:** Inserted "Convert to Text File" node to package string into a binary stream.

---

## ✅ Final Verification

- **Input:** Highlighted text in Gemini.
- **Action:** Clicked Bookmarklet -> Pasted into Popup.
- **Output:** New file `Journal Entry - 2026-01-19` created in Google Drive folder `00 - Incoming`.
