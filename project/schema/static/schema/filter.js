function myFunction() {
  // Declare variables
  var input1, input2, input3, filter, table, tr, td, i, txtValue;
  input1 = document.getElementById("Luxe").value;
  input2 = document.getElementById("Capacity").value;
  input3 = document.getElementById("Price").value;
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 1; i < tr.length; i++) {
    td1 = tr[i].getElementsByTagName("td")[1].innerText;
    td2 = tr[i].getElementsByTagName("td")[2].innerText;
    td3 = tr[i].getElementsByTagName("td")[3].innerText;

    if (td1 >= input1 && td2 >= input2 && td3 <= input3 + 1) {
      tr[i].style.display = "";
    }
    else {
      tr[i].style.display = "none";
    }
  }
}
