let input = document.getElementById("inputbox");
let btn = document.querySelectorAll("button");
btn.forEach((button) => {
  button.addEventListener("click", (e) => {
    let text = e.target.innerText;
    if (text === "AC") {
      input.value = "";
    } else if (text === "DEL") {
      input.value = input.value.slice(0, -1);
    } else if (text === "=") {
      calculation();
    } else {
      input.value += text;
    }
  });
});

async function calculation() {
  try {
    let response = await fetch("http://127.0.0.1:8000/calculate/", {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({ expression: input.value }),
    });
    let data = await response.json();
    input.value = data.result;
  } catch (error) {
    input.value = "Error";
  }
}
