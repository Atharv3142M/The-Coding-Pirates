document.addEventListener("DOMContentLoaded", loadBlogs);

function loadBlogs() {
    fetch("/api/blogs/")  // Fetch blogs from Django backend
        .then(response => response.json())
        .then(blogs => {
            const container = document.getElementById("blogsContainer");

            if (blogs.length === 0) {
                container.innerHTML = "<p>No blogs available.</p>";
                return;
            }

            blogs.forEach((blog) => {
                container.appendChild(blogTemplate(blog));
            });
        })
        .catch(error => console.error("Error fetching blogs:", error));
}

function blogTemplate(blog) {
    const blogElement = document.createElement("div");
    blogElement.classList.add("blog");

    const title = document.createElement("h2");
    title.textContent = blog.title;  // Assuming blogs now have titles

    const author = document.createElement("p");
    author.textContent = `Posted by ${blog.username}`;

    const content = document.createElement("div");
    content.innerHTML = blog.content;

    blogElement.appendChild(title);
    blogElement.appendChild(author);
    blogElement.appendChild(content);
    
    return blogElement;
}
