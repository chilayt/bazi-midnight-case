"use strict";

const choices = document.querySelector(".choices");
const buttons = choices.querySelectorAll("button");
const answer = document.getElementById("answer");

const explanations = {
  xin: "Yes. Xin is Yin Metal. It sits at the top of the Day column.",
  wu: "Wu corresponds to the Horse. Try the upper character in the Day column.",
};

for (const button of buttons) {
  button.addEventListener("click", () => {
    for (const option of buttons) option.setAttribute("aria-pressed", String(option === button));
    answer.textContent = explanations[button.dataset.choice];
  });
}
choices.hidden = false;
