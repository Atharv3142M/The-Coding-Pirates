// Quill editor
const quill = new Quill('#quill-editor', {
    theme: 'snow',
    placeholder: 'Write your post...',
    modules: {
        toolbar: [
            [{ header: [1, 2, false] }],
            ['bold', 'italic', 'underline', 'strike'],
            [{ list: 'ordered'}, { list: 'bullet' }],
            ['link', 'image'],
            ['clean']
        ]
    }
});

// Save function to send data to the backend
async function saveBlog() {
    const title = document.getElementById("title").value;
    const content = quill.root.innerHTML;
    const labels = document.getElementById("labels").value;
    const publishDate = document.getElementById("publishDate").value;
    const publishTime = document.getElementById("publishTime").value;
    const permalink = document.getElementById("permalink").value;
    const location = document.getElementById("location").value;

    if (!title || !content) {
        alert("Title and content cannot be empty.");
        return;
    }

    const blogPost = {
        title,
        content,
        labels,
        publishDate,
        publishTime,
        permalink,
        location
    };

    try {
        const response = await fetch('/save-blog/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()  // Include CSRF token
            },
            body: JSON.stringify(blogPost)
        });

        const data = await response.json();

        if (data.status === "success") {
            alert("Blog published successfully!");
            window.location.href = "/blogs";  // Redirect to blog list page
        } else {
            alert(`Error: ${data.message}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to publish blog.");
    }
}

// Function to get CSRF token
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}
