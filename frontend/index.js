        // Use /api prefix for docker-compose nginx proxy, or direct backend URL for local dev
        const BASE_URL = window.location.hostname === 'localhost' && window.location.port === '5500'
            ? "http://127.0.0.1:8000"  // Local dev (python -m http.server)
            : "/api";                   // Docker/production (nginx proxy)
        const chatWindow = document.getElementById('chat-window');
        const uploadForm = document.getElementById('upload-form');
        const fileInput = document.getElementById('file-upload');
        const fileNameDisplay = document.getElementById('file-name-display');
        const uploadButton = document.getElementById('upload-button');
        const chatForm = document.getElementById('chat-form');
        const questionInput = document.getElementById('question-input');
        const clearDbButton = document.getElementById('clear-db-button');

        // Helper to display messages in the chat window
        /**
         * @param {'user'|'system'|'api'} sender
         * @param {string} message
         * @param {boolean} isError
         */
        function displayMessage(sender, message, isError = false) {
            const messageElement = document.createElement('div');
            messageElement.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'}`;

            let bgColor = 'bg-gray-600';
            let textColor = 'text-white';
            let borderRadius = sender === 'user' ? 'rounded-br-none' : 'rounded-tl-none';
            let senderLabel = sender === 'user' ? 'You' : (sender === 'system' ? 'System' : 'RAG Engine');

            if (isError) {
                bgColor = 'bg-red-800';
                senderLabel = 'Error';
            } else if (sender === 'api') {
                bgColor = 'bg-indigo-600';
            }

            messageElement.innerHTML = `
                <div class="${bgColor} ${textColor} p-3 rounded-xl ${borderRadius} max-w-3xl shadow-lg">
                    <p class="text-sm font-semibold mb-1">${senderLabel}</p>
                    <p class="whitespace-pre-wrap">${message}</p>
                </div>
            `;
            chatWindow.appendChild(messageElement);
            // Scroll to the latest message
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }

        // --- Event Listeners ---

        // 1. File Input Change
        fileInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                fileNameDisplay.textContent = file.name;
                uploadButton.disabled = false;
                uploadButton.classList.remove('opacity-50', 'cursor-not-allowed');
            } else {
                fileNameDisplay.textContent = 'Choose Document (.pdf, .txt, .docx)';
                uploadButton.disabled = true;
                uploadButton.classList.add('opacity-50', 'cursor-not-allowed');
            }
        });

        // 2. Upload Form Submission
        uploadForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const file = fileInput.files[0];
            if (!file) {
                displayMessage('system', 'Please select a file to upload.', true);
                return;
            }

            uploadButton.disabled = true;
            uploadButton.textContent = 'Uploading...';

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch(`${BASE_URL}/upload`, {
                    method: 'POST',
                    body: formData,
                });

                const result = await response.json();

                if (!response.ok) {
                    throw new Error(result.detail || `HTTP Error: ${response.status}`);
                }
                
                displayMessage('system', result.message);

            } catch (error) {
                console.error('Upload Error:', error);
                displayMessage('system', `Upload failed: ${error.message}`, true);
            } finally {
                uploadButton.disabled = false;
                uploadButton.textContent = 'Upload';
                // Clear the input after successful upload (or failure)
                fileInput.value = '';
                fileNameDisplay.textContent = 'Choose Document (.pdf, .txt, .docx)';
                uploadButton.disabled = true;
            }
        });

        // 3. Chat Form Submission (Ask Question)
        chatForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const question = (questionInput.value || "").trim();


            if (!question) return;

            displayMessage('user', question);
            questionInput.value = '';
            questionInput.disabled = true;

            try {
                // Send the question in the JSON body (more RESTful and flexible).
                const response = await fetch(`${BASE_URL}/ask`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: question }),
                });

                const result = await response.json();

                if (!response.ok) {
                    // Assuming the backend returns a JSON error structure like {"detail": "..."}
                    questionInput.value = '';
                    questionInput.disabled = true;
                    throw new Error(result.detail || `HTTP Error: ${response.status}`);
                }
                
                // Format the API response nicely
                const formattedResponse = `Answer: ${result.response}\n\nSources:\n${result.sources.join('\n')}`;

                displayMessage('api', formattedResponse);

            } catch (error) {
                console.error('Ask Question Error:', error);
                displayMessage('system', `Request failed: ${error.message}. Did you upload a document?`, true);
            } finally {
                questionInput.disabled = false;
                questionInput.focus();
            }
        });

        // 4. Clear DB Button Click
        clearDbButton.addEventListener('click', async () => {
            if (!confirm('Are you sure you want to clear the vector database? This cannot be undone.')) {
                return;
            }

            clearDbButton.disabled = true;
            clearDbButton.textContent = 'Clearing...';

            try {
                const response = await fetch(`${BASE_URL}/clearDB`, {
                    method: 'GET',
                });
                
                const result = await response.json();

                if (!response.ok) {
                    throw new Error(result.detail || `HTTP Error: ${response.status}`);
                }
                
                displayMessage('system', result.message);
                
            } catch (error) {
                console.error('Clear DB Error:', error);
                displayMessage('system', `Clear DB failed: ${error.message}`, true);
            } finally {
                clearDbButton.disabled = false;
                clearDbButton.textContent = 'Clear DB';
            }
        });

        // Initial focus on the question input
        window.onload = () => {
            questionInput.focus();
        };
