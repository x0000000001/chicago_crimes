function main() {
  const modal = document.querySelector(".modal");
  const overlay = document.querySelector(".overlay");
  const openModalBtn = document.querySelector(".btn-open");
  const closeModalBtn = document.querySelector(".btn-close");

  // close modal function
  const closeModal = function () {
    modal.classList.add("hidden");
    overlay.classList.add("hidden");
    document.querySelector("body").style.overflow = "visible";
    document.body.style.overflowX = "hidden";
  };

  // close the modal when the close button and overlay is clicked
  closeModalBtn.addEventListener("click", closeModal);
  overlay.addEventListener("click", closeModal);

  // close modal when the Esc key is pressed
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !modal.classList.contains("hidden")) {
      closeModal();
    }
  });

  // open modal function
  const openModal = function () {
    modal.classList.remove("hidden");
    overlay.classList.remove("hidden");
    document.querySelector("body").style.overflow = "hidden";
    document.getElementById("viz_3").scrollIntoView();
  };
  // open modal event
  openModalBtn.addEventListener("click", openModal);
}

// Modal script

let interval = setInterval(() => {
  let modal = document.querySelector(".modal");
  if (modal !== null) {
    clearInterval(interval);
    main();
  }
}, 100);
