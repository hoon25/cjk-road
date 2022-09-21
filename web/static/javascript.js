function submitInput() {
  const university = $("#universityInput").val();
  if (university == "") {
    alert("대학명을 입력해주세요.");
    window.location.reload();
  } else {
    self.location.href = `/rest/${university}맛집`;
  }
}

// function submitRate() {
//   const targetCard = event.currentTarget.parentElement.parentElement;

//   // console.log(targetCard);
//   const fullTargetId = targetCard.getAttribute("id");
//   const i = fullTargetId.indexOf(" ");
//   const targetId = fullTargetId.slice(i + 1, -3);

//   const checkedRate = document.querySelector(
//     "input[name='rate-radio']:checked"
//   );
//   if (checkedRate != null) {
//     const rateValue =
//       checkedRate.parentElement.querySelector("label").innerText;

//     console.log(rateValue);
//   } else {
//     alert("nothing checked");
//   }
// }
function enterInput() {
  if (window.event.keyCode == 13) {
    submitInput();
  }
}
