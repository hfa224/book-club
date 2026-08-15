
//const polaroid = document.querySelector('.polaroid');

function closeDetails(e) {
  const polaroidDetail = document.querySelector('#polaroid_detail');
  if (polaroidDetail.open) {
    polaroidDetail.open = false;
  }
}