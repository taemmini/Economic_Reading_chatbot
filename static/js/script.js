const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const imageUpload = document.getElementById('image-upload');
const uploadButton = document.getElementById('upload-button');
const imagePreviewContainer = document.getElementById('image-preview-container');
const imagePreview = document.getElementById('image-preview');
const removeImageButton = document.getElementById('remove-image');
const dragArea = document.getElementById('drag-area');

let currentImage = null;

// 드래그 앤 드롭 이벤트 처리
dragArea.addEventListener('dragenter', (e) => {
    e.preventDefault();
    dragArea.classList.add('border-blue-500', 'bg-blue-50');
});

dragArea.addEventListener('dragover', (e) => {
    e.preventDefault();
});

dragArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dragArea.classList.remove('border-blue-500', 'bg-blue-50');
});

dragArea.addEventListener('drop', async (e) => {
    e.preventDefault();
    dragArea.classList.remove('border-blue-500', 'bg-blue-50');

    const file = e.dataTransfer.files[0];
    await handleImageFile(file);
    // 이미지만 있는 경우 자동으로 전송
    if (!userInput.value.trim()) {
        sendMessage();
    }
});

async function handleImageFile(file) {
    if (file) {
        // 이미지 파일인지 확인
        if (!file.type.startsWith('image/')) {
            alert('이미지 파일만 업로드 가능합니다.');
            return;
        }

        // 파일 크기 확인 (20MB)
        if (file.size > 20 * 1024 * 1024) {
            alert('파일 크기는 20MB를 초과할 수 없습니다.');
            return;
        }

        currentImage = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreviewContainer.classList.remove('hidden');
            dragArea.classList.add('hidden');

            // 텍스트 입력이 없는 경우 자동으로 전송
            if (!userInput.value.trim()) {
                sendMessage();
            }
        };
        reader.readAsDataURL(file);
    }
}

// 이미지 업로드 버튼 클릭 처리
uploadButton.addEventListener('click', () => {
    imageUpload.click();
});

imageUpload.addEventListener('change', (e) => {
    const file = e.target.files[0];
    handleImageFile(file);
});

// 이미지 제거
removeImageButton.addEventListener('click', clearImagePreview);

function clearImagePreview() {
    currentImage = null;
    imagePreview.src = '';
    imagePreviewContainer.classList.add('hidden');
    dragArea.classList.remove('hidden');
    imageUpload.value = '';
}

function addMessage(message, isUser = false, image = null) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('p-3', 'rounded-lg', 'max-w-3/4', 'mb-4');
    messageElement.classList.add(isUser ? 'user-message' : 'bot-message');
    messageElement.classList.add(isUser ? 'ml-auto' : 'mr-auto');

    if (image) {
        messageElement.classList.add('message-with-image');
        const imageElement = document.createElement('img');
        imageElement.src = image;
        imageElement.classList.add('message-image');
        messageElement.appendChild(imageElement);
    }

    const textElement = document.createElement('div');
    textElement.classList.add('text-gray-800', 'message-content');
    textElement.innerHTML = message.replace(/\n/g, '<br>');

    messageElement.appendChild(textElement);
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage(message = null) {
    const formData = new FormData();

    if (!message && !currentImage) {
        return;
    }

    if (message) {
        formData.append('question', message);
    }

    let imageUrl;
    if (currentImage) {
        formData.append('image', currentImage);
    }

    // 메시지 추가는 한 번만 실행
    if (message || currentImage) {
        if (currentImage) {
            imageUrl = URL.createObjectURL(currentImage);
            addMessage(message || '', true, imageUrl);
        } else {
            addMessage(message, true);
        }
    }

    userInput.value = '';
    adjustTextareaHeight();
    clearImagePreview();

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('네트워크 환경이 좋지 않습니다. 다시 시도해주세요.');
        }

        const data = await response.json();
        addMessage(data.answer);
    } catch (error) {
        console.error('Error:', error);
        addMessage('요청을 처리하는데 문제가 발생했습니다.');
    }
}

chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (message || currentImage) {
        sendMessage(message);
    }
});

function adjustTextareaHeight() {
    userInput.style.height = 'auto';
    userInput.style.height = (userInput.scrollHeight) + 'px';
}

// textarea 자동 크기 조절
userInput.addEventListener('input', adjustTextareaHeight);

// 디바운스 함수
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

const debouncedAdjustTextareaHeight = debounce(adjustTextareaHeight, 100);
userInput.addEventListener('input', debouncedAdjustTextareaHeight);

// Enter 키 처리
userInput.addEventListener('keydown', (e) => {
    if (e.isComposing) return; // 조합 중일 때 Enter 키 입력을 무시
    if (e.key === 'Enter') {
        if (!e.shiftKey) {
            e.preventDefault();
            const message = userInput.value.trim();
            if (message || currentImage) {
                sendMessage(message);
            }
        }
    }
});

// 클립보드 붙여넣기 이벤트 리스너 
document.addEventListener('paste', async (e) => {
    const items = e.clipboardData.items;

    for (const item of items) {
        if (item.type.startsWith('image')) {
            e.preventDefault(); 
            const file = item.getAsFile();
            await handleImageFile(file);
            break;
        }
        // 텍스트인 경우 기본 붙여넣기 동작 허용
    }
});