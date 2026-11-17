"use strict";

const choices = document.querySelector(".choices");
const buttons = choices.querySelectorAll("button");
const answer = document.getElementById("answer");

for (const button of buttons) {
  button.addEventListener("click", () => {
    for (const option of buttons) option.setAttribute("aria-pressed", String(option === button));
    answer.textContent = button.dataset.explanation;
  });
}
choices.hidden = false;
