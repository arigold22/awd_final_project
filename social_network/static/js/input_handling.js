function usernameCheck() {
  var username = document.getElementById("username").value;
  var usernameIllegalCharacters = /^[a-zA-Z0-9]+$/;
  if (username.length >= 4 && username.length <= 16) {
    greenLength();
  } else {
    redLength();
  }
  if (usernameIllegalCharacters.test(username)) {
    greenLetter();
  } else {
    redLetter();
  }
  if (username.length == 0) {
    emptyInput();
  }
}

function greenLetter() {
  document.getElementById("usernameLetters").style.color = "green";
  document.getElementById("usernameLettersCross").style.display = "none";
  document.getElementById("usernameLettersTick").style.display = "inline";
}

function greenLength() {
  document.getElementById("usernameLength").style.color = "green";
  document.getElementById("usernameLengthCross").style.display = "none";
  document.getElementById("usernameLengthTick").style.display = "inline";
}

function redLetter() {
  document.getElementById("usernameLetters").style.color = "red";
  document.getElementById("usernameLettersCross").style.display = "inline";
  document.getElementById("usernameLettersTick").style.display = "none";
}

function redLength() {
  document.getElementById("usernameLength").style.color = "red";
  document.getElementById("usernameLengthCross").style.display = "inline";
  document.getElementById("usernameLengthTick").style.display = "none";
}

function emptyInput() {
  document.getElementById("usernameLetters").style.color = "grey";
  document.getElementById("usernameLettersCross").style.display = "inline";
  document.getElementById("usernameLettersTick").style.display = "none";
  document.getElementById("usernameLength").style.color = "grey";
  document.getElementById("usernameLengthCross").style.display = "inline";
  document.getElementById("usernameLengthTick").style.display = "none";
}

