function showDetails(title, author, description) {
    document.getElementById("popup").style.display = "flex";
    document.getElementById("book-title").innerText = title;
    document.getElementById("book-author").innerText = author;
    document.getElementById("book-description").innerText = description;
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}
