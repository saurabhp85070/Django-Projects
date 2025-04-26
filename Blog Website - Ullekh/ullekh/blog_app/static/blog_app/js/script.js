document.addEventListener('DOMContentLoaded', function() {
    const commentSection = document.querySelector('.col-lg-8');
    const postId = document.querySelector('#detail-body').dataset.postId;

    // Function to close all open forms and menus
    function closeAllFormsAndMenus() {
        document.querySelectorAll('.edit-comment-form, .reply-form').forEach(form => {
            form.style.display = 'none';
        });
        document.querySelectorAll('.comment-text').forEach(text => {
            text.style.display = 'block';
        });
        document.querySelectorAll('.comment-menu-options').forEach(menu => {
            menu.style.display = 'none';
        });
    }

    // Toggle comment menu options
    commentSection.addEventListener('click', function(e) {
        if (e.target.classList.contains('toggle-menu') || e.target.closest('.toggle-menu')) {
            e.preventDefault();
            e.stopPropagation();
            closeAllFormsAndMenus();
            const button = e.target.closest('.toggle-menu');
            const options = button.nextElementSibling;
            options.style.display = options.style.display === 'none' ? 'block' : 'none';
        }
    });

    // Hide menu options when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.comment-menu') && !e.target.closest('.edit-comment-form') && !e.target.closest('.reply-form')) {
            closeAllFormsAndMenus();
        }
    });

    // Toggle reply form
    commentSection.addEventListener('click', function(e) {
        if (e.target.classList.contains('reply-link')) {
            e.preventDefault();
            closeAllFormsAndMenus();
            const commentId = e.target.closest('.comment').id.split('-')[1];
            const replyForm = document.getElementById(`comment-${commentId}`).querySelector('.reply-form');
            replyForm.style.display = 'block';
        }
    });

    // Show edit form
    commentSection.addEventListener('click', function(e) {
        if (e.target.classList.contains('edit-comment-link')) {
            e.preventDefault();
            closeAllFormsAndMenus();
            const commentId = e.target.dataset.commentId;
            const commentDiv = document.getElementById(`comment-${commentId}`);
            const commentText = commentDiv.querySelector('.comment-text');
            const editForm = commentDiv.querySelector('.edit-comment-form');
            
            commentText.style.display = 'none';
            editForm.style.display = 'block';
        }
    });

    // Cancel edit
    commentSection.addEventListener('click', function(e) {
        if (e.target.classList.contains('cancel-edit')) {
            e.preventDefault();
            const form = e.target.closest('.edit-comment-form');
            const commentDiv = form.closest('.comment');
            const commentText = commentDiv.querySelector('.comment-text');
            
            form.style.display = 'none';
            commentText.style.display = 'block';
        }
    });

    // Cancel reply
    commentSection.addEventListener('click', function(e) {
        if (e.target.classList.contains('cancel-reply')) {
            e.preventDefault();
            const replyForm = e.target.closest('.reply-form');
            replyForm.style.display = 'none';
        }
    });

    // Delete comment
    commentSection.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-comment-link')) {
            e.preventDefault();
            const commentId = e.target.dataset.commentId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/detail/${postId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: `action=delete_comment&comment_id=${commentId}`,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const commentElement = document.getElementById(`comment-${commentId}`);
                    if (commentElement) {
                        commentElement.remove();
                        // Update total comments count
                        const totalCommentsElement = document.querySelector('h3.mb-4');
                        if (totalCommentsElement) {
                            const currentCount = parseInt(totalCommentsElement.textContent.match(/\d+/)[0]);
                            const newCount = currentCount - data.deleted_count;
                            totalCommentsElement.textContent = `Comments(${newCount})`;
                        }
                    }
                    // Display success message
                    showMessage(data.message, 'success');
                } else {
                    console.error('Error deleting comment:', data.error);
                    showMessage(data.error, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('An error occurred while deleting the comment', 'error');
            });
        }
    });

    // Function to show messages
    function showMessage(message, type) {
        const messageContainer = document.getElementById('message-container');
        if (!messageContainer) {
            console.error('Message container not found');
            return;
        }

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-dismissible fade show alert-${type === 'success' ? 'success' : 'danger'}`;
        alertDiv.role = 'alert';

        const strongElement = document.createElement('strong');
        strongElement.textContent = message;

        const closeButton = document.createElement('button');
        closeButton.type = 'button';
        closeButton.className = 'btn-close';
        closeButton.setAttribute('data-bs-dismiss', 'alert');
        closeButton.setAttribute('aria-label', 'Close');

        alertDiv.appendChild(strongElement);
        alertDiv.appendChild(closeButton);
        messageContainer.appendChild(alertDiv);

        // Remove the message after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    // Save/Unsave post functionality
    const saveBtn = document.querySelector('.save-btn');
    if (saveBtn) {
        saveBtn.addEventListener('click', function() {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/detail/${postId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: `action=toggle_save&post_id=${postId}`,
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_saved) {
                    this.classList.add('saved');
                    this.title = 'Unsave Post';
                    this.querySelector('i').classList.replace('fa-regular', 'fa-solid');
                } else {
                    this.classList.remove('saved');
                    this.title = 'Save Post';
                    this.querySelector('i').classList.replace('fa-solid', 'fa-regular');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Function to scroll to a specific element with offset
    function scrollToElementWithOffset(elementId, offset) {
        const element = document.getElementById(elementId);
        if (element) {
            const elementPosition = element.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - offset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    }

    // Scroll to the target comment if present in the URL
    const hash = window.location.hash;
    if (hash) {
        // Wait for the page to load completely
        window.addEventListener('load', function() {
            setTimeout(function() {
                const commentId = hash.slice(1); // Remove the '#' from the hash
                const navbarHeight = document.querySelector('nav').offsetHeight; // Get the navbar height
                const additionalOffset = 20; // Additional offset for better visibility
                scrollToElementWithOffset(commentId, navbarHeight + additionalOffset);
            }, 100); // Small delay to ensure everything is rendered
        });
    }

    // Add this function to handle form submissions
    function handleFormSubmit(event) {
        const form = event.target;
        if (form.method === 'post') {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                })
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newContent = doc.querySelector('#detail-body');
                    document.querySelector('#detail-body').innerHTML = newContent.innerHTML;

                    // Get the newly added comment ID from the response
                    const newCommentId = doc.querySelector('.comment:last-child').id;
                    
                    // Scroll to the new comment
                    const navbarHeight = document.querySelector('nav').offsetHeight;
                    const additionalOffset = 20;
                    scrollToElementWithOffset(newCommentId, navbarHeight + additionalOffset);
                })
                .catch(error => console.error('Error:', error));
            });
        }
    }

    // Add event listeners for form submissions
    document.querySelectorAll('form').forEach(form => {
        handleFormSubmit(form);
    });

    // Add this new code for the download button
    const downloadBtn = document.querySelector('.download-btn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const downloadUrl = `/blog/${postId}/download/`;
            const icon = this.querySelector('i');
            
            // Show loading animation
            icon.classList.remove('fa-file-download');
            icon.classList.add('fa-spinner', 'fa-spin');
            
            // Fetch the PDF
            fetch(downloadUrl)
                .then(response => response.blob())
                .then(blob => {
                    // Create a temporary URL for the blob
                    const url = window.URL.createObjectURL(blob);
                    
                    // Create a temporary anchor element and trigger the download
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = 'blog_post.pdf';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    
                    // Restore the original icon
                    icon.classList.remove('fa-spinner', 'fa-spin');
                    icon.classList.add('fa-file-download');
                })
                .catch(error => {
                    console.error('Download failed:', error);
                    // Restore the original icon
                    icon.classList.remove('fa-spinner', 'fa-spin');
                    icon.classList.add('fa-file-download');
                    alert('Download failed. Please try again.');
                });
        });
    }



});

// profile script:
// New function for profile page functionality
function initializeProfilePage() {
    const navLinks = document.querySelectorAll('.profile-nav-link');
    const tabContents = document.querySelectorAll('.tab-content');

    function showTab(tabId) {
        tabContents.forEach(content => {
            if (content.id === tabId) {
                content.style.display = 'block';
            } else {
                content.style.display = 'none';
            }
        });
        
        navLinks.forEach(link => {
            if (link.getAttribute('data-tab') === tabId) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const tabId = this.getAttribute('data-tab');
            showTab(tabId);
            history.pushState(null, '', `?tab=${tabId}`);
        });
    });

    // Handle back/forward browser navigation
    window.addEventListener('popstate', function() {
        const tabId = new URLSearchParams(window.location.search).get('tab') || 'about';
        showTab(tabId);
    });

    // Show initial tab
    const initialTab = new URLSearchParams(window.location.search).get('tab') || 'about';
    showTab(initialTab);
}

// Call initializeProfilePage() when the DOM is loaded, but only if we're on the profile page
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.profile-container')) {
        initializeProfilePage();
    }
});