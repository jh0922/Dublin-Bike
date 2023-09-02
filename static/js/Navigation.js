window.onload=function(){
const pageList = document.getElementById('pagelist');
  const pageContent = document.getElementById('wholePage');

  pageList.addEventListener('click', (event) => {
    const page = event.target.dataset.page;
    if (page) {
      fetch(`/${page}`)
        .then(response => response.text())
        .then(html => {
          pageContent.innerHTML = html;
        });
    }
  });
};
// const homepage = document.getElementById('home');
// const pageContent = document.getElementById('wholePage');
// homepage.addEventListener('click', (event) => {
//     fetch("/")
//     .then(response => response.text())
//     .then(html => {
//       pageContent.innerHTML = html;
//     });
// })