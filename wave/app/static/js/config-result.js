const provisionUp = document.getElementById("provision-up");
const provisionLoading = document.getElementById("provision-loading");
const rootMessage = document.getElementById("root-message");

provisionUp.addEventListener("click", () => {
    provisionUp.style.display = "none";
    provisionLoading.style.display = "inline-block";
    rootMessage.style.display = "block";
});
