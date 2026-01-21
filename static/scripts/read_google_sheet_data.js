// external js: isotope.pkgd.js

// Replace with your actual Spreadsheet ID
const spreadsheetId = "1r9oKI47-_qaL_45qixRrOVO5_WsqmMUyHAhl3r8r3d0";

// Replace with your API Key
const apiKey = "AIzaSyChKod4X-iB9laGOWxGJ3UvZWWK56slY0Q";

function dateParse(dateString) {
  const month_year = dateString.split("-");
  console.log(month_year[0])
  console.log(month_year[1])
  return new Date(parseInt(month_year[1]), parseInt(month_year[0])-1)
}

// init Isotope
function initIsotope() {
  var $grid = $('.book-container').isotope({
    itemSelector: '.book-item',
    layoutMode: 'fitRows',
    sortAscending: {
      rating: false
    },
    getSortData: {
      title: '.title',
      author: '.author',
      genre: '.genre',
      year: '.year parseInt',
      average: '.average parseFloat',
      picker: '[data-category]'
    }
  });

  // bind filter button click
  $('#filters').on('click', 'button', function () {
    var filterValue = $(this).attr('data-filter');
    // use filterFn if matches value
    //filterValue = filterFns[ filterValue ] || filterValue;
    $grid.isotope({ filter: filterValue });
  });

  // bind sort button click
  $('#sorts').on('click', 'button', function () {
    var sortByValue = $(this).attr('data-sort-by');
    $grid.isotope({ sortBy: sortByValue });
  });

  // change is-checked class on buttons
  $('.button-group').each(function (i, buttonGroup) {
    var $buttonGroup = $(buttonGroup);
    $buttonGroup.on('click', 'button', function () {
      $buttonGroup.find('.is-checked').removeClass('is-checked');
      $(this).addClass('is-checked');
    });
  });
}

// https://docs.google.com/spreadsheets/d/1r9oKI47-_qaL_45qixRrOVO5_WsqmMUyHAhl3r8r3d0/edit?usp=sharing

// Construct the URL for Google Sheets API v4
const url = `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values/Sheet1?key=${apiKey}`;

const img_url = 'https://berlinbeerbook.club/static/images/book_covers/'

async function fetchGoogleSheetData() {
  try {
    // Fetch data from Google Sheets API
    const response = await fetch(url);
    const data = await response.json();

    // Extract rows from the data
    const rows = data.values;

    // Get the table body element
    const book_container = document.querySelector(".book-container");

    // Column key
    // 0 - Title
    // 1 - Author
    // 2 - Year
    // 3 - Picker
    // 4 - Date
    // 5 - H rating
    // 6 - M rating
    // 7 - B rating
    // 8 - Genre
    // 9 - Average (could just calculate?)

    var ratingMap = {
      5: "🌟",
      4: "😊",
      3: "😐",
      2: "😞",
      1: "😖",
      "dnf": "🚫"
    };

    listOfBooks = []
    listOfRatings = []

    for (let i = 1; i < rows.length; i++) {
      const row = rows[i];

      // class name vs value
      const bookMap = {
        "title": row[0],
        "author": row[1],
        "year": row[2],
        "picker": row[3],
        "date": dateParse(row[4]),
        "genre": row[8],
        "average": row[9]
      }

      listOfBooks[i] = bookMap;

      const ratingsMap = {
        "Helen": row[5],
        "Max": row[6],
        "Beth": row[7]
      };

      listOfRatings[i] = ratingsMap;

    }

    // TODO sort ratings
    // listOfBooks.sort(function(a, b) { 
    //   return a["date"] - b["date"];
    // })

    // Loop through the rows (starting from row 1 to skip headers)
    for (let i = 1; i < listOfBooks.length; i++) {

      const bookMap = listOfBooks[i];
      const ratingsMap = listOfRatings[i];


      const book_div = document.createElement("div");
      const book_cover = document.createElement("div");
      book_cover.setAttribute("class", "book-cover");
      const book_info = document.createElement("div");
      book_info.setAttribute("class", "book-info");
      book_div.appendChild(book_cover);
      book_div.appendChild(book_info);


      // construct the book div
      book_div.setAttribute("class", "book-item " + bookMap["picker"]);
      book_div.setAttribute("data-category", bookMap["picker"]);

      //https://berlinbeerbook.club/static/images/book_covers/vampire_blood_trilogy_darren_shan.jpg
      var url_title = bookMap["title"].trim().replaceAll(" ", "_").replace(/\W+/g, "").toLowerCase();
      var url_author = bookMap["author"].trim().replaceAll(" ", "_").replace(/\W+/g, "").toLowerCase();

      var imgElement = document.createElement("img");
      const book_cover_url = img_url + url_title + "_" + url_author + ".jpg";
      console.log(book_cover_url);
      imgElement.setAttribute("src", book_cover_url);

      book_cover.appendChild(imgElement);

      for (const [key, value] of Object.entries(bookMap)) {
        const title_p = document.createElement("p");
        title_p.setAttribute("class", key);
        if (key == "date") {
          const month = value.toLocaleString('default', { month: 'short' });
          const year = value.toLocaleString('default', { year: 'numeric' });
          title_p.innerText = month + " " + year
        } else {
          title_p.innerText = value;
        }
        book_info.appendChild(title_p)
      }

      for (const [key, value] of Object.entries(ratingsMap)) {
        const title_p = document.createElement("p");
        //title_p.setAttribute("class", key);
        if (value != "dnf") {
        title_p.innerText = key + ": " + ratingMap[Math.round(value)];
        } else {
        title_p.innerText = key + ": " + ratingMap[Math.round("dnf")];
        }
        book_info.appendChild(title_p)
      }

      book_container.appendChild(book_div)
    }

  } catch (error) {
    console.error("Error fetching Google Sheets data:", error);
  } finally {
    initIsotope();
  }
}

// Call the function to fetch and display data
document.addEventListener("DOMContentLoaded", fetchGoogleSheetData);