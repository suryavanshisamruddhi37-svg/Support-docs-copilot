
"use strict";

// ============================================================
// SUPPORT DOCS COPILOT - FRONTEND LOGIC
// ============================================================

const API_BASE_URL = "http://127.0.0.1:8000";

// DOM helper: supports alternate IDs in redesigned HTML.
function getElement(...ids) {
    for (const id of ids) {
        const element = document.getElementById(id);
        if (element) return element;
    }
    return null;
}

// ============================================================
// DOM ELEMENTS
// ============================================================

const sidebar = getElement("sidebar");
const sidebarBackdrop = getElement("sidebarBackdrop");
const openSidebarBtn = getElement("openSidebarBtn");
const closeSidebarBtn = getElement("closeSidebarBtn");
const newChatBtn = getElement("newChatBtn");

const fileInput = getElement("fileInput", "documentInput", "uploadInput");
const dropZone = getElement("dropZone", "uploadZone", "uploadArea");

const uploadProgressBox = getElement("uploadProgressBox", "uploadProgress");
const uploadProgressBar = getElement("uploadProgressBar", "progressBar");
const uploadStatusText = getElement("uploadStatusText", "uploadStatus");
const uploadFileName = getElement("uploadFileName");

const uploadErrorBox = getElement("uploadErrorBox", "uploadError");
const uploadErrorText = getElement("uploadErrorText", "uploadErrorMessage");

const activeDocCard = getElement("activeDocCard", "documentCard");
const activeDocName = getElement("activeDocName", "documentName");
const activeDocChunks = getElement("activeDocChunks", "documentChunks");
const removeDocBtn = getElement("removeDocBtn");

const headerDocBadge = getElement("headerDocBadge", "documentBadge");
const headerDocNameBadge = getElement("headerDocNameBadge", "documentBadgeName");

const welcomeState = getElement("welcomeState", "welcomeScreen");
const messageList = getElement("messageList", "messages", "chatMessages");
const typingIndicator = getElement("typingIndicator");

const chatForm = getElement("chatForm");
const questionInput = getElement("questionInput", "messageInput", "chatInput");
const sendBtn = getElement("sendBtn", "sendButton");

const backendIndicator = getElement("backendIndicator");
const backendStatusText = getElement("backendStatusText");

const toast = getElement("toast");
const toastIcon = getElement("toastIcon");
const toastMessage = getElement("toastMessage");

// ============================================================
// STATE
// ============================================================

let currentDocument = null;
let isUploading = false;
let isAsking = false;

// ============================================================
// TOAST NOTIFICATIONS
// ============================================================

function showToast(message, type = "success") {
    if (!toast || !toastMessage) {
        console.log(`[${type}] ${message}`);
        return;
    }

    toastMessage.textContent = message;

    if (toastIcon) {
        const iconClasses = {
            success: "fa-solid fa-circle-check text-emerald-400",
            error: "fa-solid fa-circle-exclamation text-red-400",
            info: "fa-solid fa-circle-info text-blue-400"
        };

        toastIcon.className = iconClasses[type] || iconClasses.success;
    }

    toast.classList.remove(
        "translate-y-20",
        "translate-x-[120%]",
        "opacity-0"
    );

    toast.classList.add("translate-y-0", "translate-x-0", "opacity-100");

    clearTimeout(showToast.timeout);

    showToast.timeout = setTimeout(() => {
        toast.classList.add("translate-y-20", "opacity-0");
        toast.classList.remove("translate-y-0", "opacity-100");
    }, 3000);
}

// ============================================================
// SIDEBAR
// ============================================================

function toggleSidebar() {
    if (!sidebar) return;

    sidebar.classList.toggle("-translate-x-full");

    if (sidebarBackdrop) {
        sidebarBackdrop.classList.toggle("hidden");
    }
}

function closeSidebar() {
    sidebar?.classList.add("-translate-x-full");
    sidebarBackdrop?.classList.add("hidden");
}

openSidebarBtn?.addEventListener("click", toggleSidebar);
closeSidebarBtn?.addEventListener("click", closeSidebar);
sidebarBackdrop?.addEventListener("click", closeSidebar);

// ============================================================
// FILE UPLOAD
// ============================================================

// FIX: clicking anywhere on the upload area opens the file picker.
if (dropZone && fileInput) {
    dropZone.addEventListener("click", (event) => {
        // Avoid recursively triggering clicks on the input itself.
        if (event.target === fileInput) return;

        // Do not open the picker when clicking an unrelated button.
        if (event.target.closest("button")) return;

        fileInput.click();
    });

    dropZone.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropZone.classList.add("border-blue-500", "bg-blue-50");
    });

    dropZone.addEventListener("dragleave", (event) => {
        if (!dropZone.contains(event.relatedTarget)) {
            dropZone.classList.remove("border-blue-500", "bg-blue-50");
        }
    });

    dropZone.addEventListener("drop", (event) => {
        event.preventDefault();
        dropZone.classList.remove("border-blue-500", "bg-blue-50");

        const files = event.dataTransfer?.files;

        if (files && files.length > 0) {
            uploadFile(files[0]);
        }
    });
}

fileInput?.addEventListener("change", () => {
    const file = fileInput.files?.[0];

    if (file) {
        uploadFile(file);
    }
});

async function uploadFile(file) {
    if (isUploading) return;

    if (!file) {
        showToast("Please select a document first.", "error");
        return;
    }

    const extension = file.name.split(".").pop().toLowerCase();

    if (!["pdf", "docx"].includes(extension)) {
        showToast("Please upload a PDF or DOCX file.", "error");
        if (fileInput) fileInput.value = "";
        return;
    }

    isUploading = true;
    hideUploadError();

    if (uploadProgressBox) uploadProgressBox.classList.remove("hidden");
    if (uploadFileName) uploadFileName.textContent = file.name;
    if (uploadStatusText) uploadStatusText.textContent = "Uploading and indexing...";
    if (uploadProgressBar) uploadProgressBar.style.width = "15%";

    const formData = new FormData();
    formData.append("file", file);

    try {
        if (uploadProgressBar) uploadProgressBar.style.width = "35%";

        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: "POST",
            body: formData
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            const detail = typeof data.detail === "string"
                ? data.detail
                : "The server could not process this document.";

            throw new Error(detail);
        }

        if (uploadProgressBar) uploadProgressBar.style.width = "100%";
        if (uploadStatusText) uploadStatusText.textContent = "Indexed successfully";

        currentDocument = {
            filename: data.filename || file.name,
            chunks: data.chunks ?? data.chunk_count ?? "Indexed",
            embedding_dimension: data.embedding_dimension ?? null
        };

        updateDocumentUI();

        showToast(`${file.name} uploaded successfully.`, "success");

        setTimeout(() => {
            uploadProgressBox?.classList.add("hidden");
        }, 1500);

    } catch (error) {
        console.error("Upload error:", error);

        showUploadError(
            error.message ||
            "Upload failed. Check that the backend is running."
        );

        showToast("Document upload failed.", "error");

    } finally {
        isUploading = false;

        if (fileInput) {
            fileInput.value = "";
        }
    }
}

// ============================================================
// DOCUMENT UI
// ============================================================

function updateDocumentUI() {
    if (!currentDocument) return;

    activeDocCard?.classList.remove("hidden");
    headerDocBadge?.classList.remove("hidden");

    if (activeDocName) {
        activeDocName.textContent = currentDocument.filename;
    }

    if (activeDocChunks) {
        const count = currentDocument.chunks;
        activeDocChunks.textContent =
            typeof count === "number" ? `${count} chunks indexed` : String(count);
    }

    if (headerDocNameBadge) {
        headerDocNameBadge.textContent = currentDocument.filename;
    }

    // Allow questions after a document has been uploaded.
    if (questionInput) {
        questionInput.disabled = false;
        questionInput.placeholder = "Ask a question about your uploaded document...";
    }

    updateSendButton();
}

function removeDocument() {
    // This clears the frontend display only.
    // It does NOT delete stored vectors from ChromaDB.
    currentDocument = null;

    activeDocCard?.classList.add("hidden");
    headerDocBadge?.classList.add("hidden");

    if (headerDocNameBadge) {
        headerDocNameBadge.textContent = "No document loaded";
    }

    showToast("Document cleared from this session.", "info");
}

removeDocBtn?.addEventListener("click", removeDocument);

// ============================================================
// UPLOAD ERRORS
// ============================================================

function showUploadError(message) {
    if (uploadErrorBox) uploadErrorBox.classList.remove("hidden");

    if (uploadErrorText) {
        uploadErrorText.textContent = message;
    } else if (uploadErrorBox) {
        uploadErrorBox.textContent = message;
    }

    uploadProgressBox?.classList.add("hidden");
}

function hideUploadError() {
    uploadErrorBox?.classList.add("hidden");
}

// ============================================================
// SUGGESTED QUESTIONS
// ============================================================

function selectSuggestion(question) {
    if (!questionInput) return;

    questionInput.value = question;
    questionInput.focus();

    autoResizeTextarea();
    updateSendButton();
}

function selectStarter(question) {
    selectSuggestion(question);
    handleUserQuery(question);
}

window.selectSuggestion = selectSuggestion;
window.selectStarter = selectStarter;

// ============================================================
// CHAT
// ============================================================

chatForm?.addEventListener("submit", (event) => {
    event.preventDefault();
    handleUserQuery();
});

async function handleUserQuery(question = null) {
    if (isAsking) return;

    const userQuestion = (
        question ??
        questionInput?.value ??
        ""
    ).trim();

    if (!userQuestion) return;

    if (questionInput) {
        questionInput.value = "";
        autoResizeTextarea();
    }

    welcomeState?.classList.add("hidden");

    appendMessage("user", userQuestion);

    showTypingIndicator();
    isAsking = true;
    setSendButtonState(true);

    try {
        const response = await fetch(`${API_BASE_URL}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: userQuestion
            })
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            const detail = typeof data.detail === "string"
                ? data.detail
                : "Unable to get an answer.";

            throw new Error(detail);
        }

        hideTypingIndicator();

        appendMessage(
            "assistant",
            data.answer || "No answer was returned by the server."
        );

    } catch (error) {
        console.error("Question error:", error);
        hideTypingIndicator();

        appendMessage(
            "assistant",
            error.message ||
            "The AI service is temporarily unavailable. Please try again."
        );

        showToast("Unable to get an answer.", "error");

    } finally {
        isAsking = false;
        updateSendButton();
    }
}

// ============================================================
// CHAT MESSAGES
// ============================================================

function appendMessage(role, message) {
    if (!messageList) return;

    const wrapper = document.createElement("div");

    wrapper.className = role === "user"
        ? "flex justify-end mb-5"
        : "flex justify-start mb-5";

    const bubble = document.createElement("div");

    bubble.className = role === "user"
        ? "max-w-[85%] rounded-2xl rounded-br-md bg-blue-600 text-white px-4 py-3 shadow-sm"
        : "max-w-[90%] rounded-2xl rounded-tl-md bg-white border border-slate-200 text-slate-800 px-4 py-3 shadow-sm";

    const text = document.createElement("p");
    text.className = "text-sm leading-6 whitespace-pre-wrap break-words";
    text.textContent = message;

    bubble.appendChild(text);
    wrapper.appendChild(bubble);

    if (role === "assistant") {
        const copyButton = document.createElement("button");

        copyButton.type = "button";
        copyButton.className =
            "block mt-2 text-xs text-slate-500 hover:text-blue-600";
        copyButton.textContent = "Copy answer";

        copyButton.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(message);
                showToast("Answer copied.", "success");
            } catch (error) {
                console.error("Copy failed:", error);
                showToast("Could not copy the answer.", "error");
            }
        });

        bubble.appendChild(copyButton);
    }

    messageList.appendChild(wrapper);

    wrapper.scrollIntoView({
        behavior: "smooth",
        block: "end"
    });
}

window.handleUserQuery = handleUserQuery;

// ============================================================
// TYPING INDICATOR
// ============================================================

function showTypingIndicator() {
    typingIndicator?.classList.remove("hidden");
}

function hideTypingIndicator() {
    typingIndicator?.classList.add("hidden");
}

// ============================================================
// TEXTAREA AND SEND BUTTON
// ============================================================

function autoResizeTextarea() {
    if (!questionInput) return;

    questionInput.style.height = "auto";
    questionInput.style.height =
        Math.min(questionInput.scrollHeight, 140) + "px";
}

function updateSendButton() {
    if (!sendBtn) return;

    sendBtn.disabled =
        isAsking ||
        !questionInput ||
        questionInput.value.trim().length === 0;
}

function setSendButtonState(disabled) {
    if (!sendBtn) return;
    sendBtn.disabled = disabled;
}

questionInput?.addEventListener("input", () => {
    autoResizeTextarea();
    updateSendButton();
});

questionInput?.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();

        if (chatForm) {
            chatForm.requestSubmit();
        } else {
            handleUserQuery();
        }
    }
});

// ============================================================
// NEW CHAT
// ============================================================

function resetChat() {
    if (messageList) {
        messageList.innerHTML = "";
    }

    welcomeState?.classList.remove("hidden");

    if (questionInput) {
        questionInput.value = "";
        autoResizeTextarea();
        questionInput.focus();
    }

    hideTypingIndicator();
    updateSendButton();
    closeSidebar();

    showToast("New chat session started.", "info");
}

newChatBtn?.addEventListener("click", resetChat);

// ============================================================
// BACKEND HEALTH CHECK
// ============================================================

async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);

        if (!response.ok) {
            throw new Error("Backend returned an error.");
        }

        setBackendStatus(true, "Backend online");

    } catch (error) {
        console.error("Backend health check failed:", error);
        setBackendStatus(false, "Backend offline");
    }
}

function setBackendStatus(isOnline, message) {
    if (backendStatusText) {
        backendStatusText.textContent = message;
    }

    if (backendIndicator) {
        backendIndicator.classList.toggle("bg-emerald-500", isOnline);
        backendIndicator.classList.toggle("bg-red-500", !isOnline);
    }
}

// ============================================================
// INITIALIZATION
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
    console.log("Support Docs Copilot frontend loaded.");

    checkBackendHealth();
    autoResizeTextarea();
    updateSendButton();

    if (!fileInput) {
        console.warn(
            "Upload input not found. Check the file input ID in index.html."
        );
    }

    if (!dropZone) {
        console.warn(
            "Upload area not found. Check the upload area ID in index.html."
        );
    }
});
