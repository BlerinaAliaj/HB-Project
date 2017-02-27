// JS for trip detail page

function submitList(evt) {
  evt.preventDefault();
  var allList = {};
  var allData = {};
  var rowId;
  var desc;
  var usid;
  var comp;

  allList["tripCode"] = tripCode;

  $(".editabletable tr").each(function(){

      rowId = $(this).attr('id');
      // console.log(rowId);

      if (rowId === "addItem") {
        $('#'+rowId).each(function() {
        desc = $(this).find('#indesc').val();
        usid = $(this).find('#inusid').val();
        comp = $(this).find('#incomp').is(":checked");

        // console.log(comp);

        allData[rowId] = {"description": desc,
                        "userid": usid,
                        "completed": comp}; });
      } else {

        $('#'+rowId).each(function() {
        desc = $(this).find('#desc').text();
        usid = $(this).find('#usid').text();
        comp = $(this).find('#comp').text();
        console.log(comp);

        allData[rowId] = {"description": desc,
                        "userid": usid,
                        "completed": comp}; });
      }
  });
  allList['allData'] = JSON.stringify(allData);
  console.log(allList);

  $.post("/list.json", allList, function(){ alert("it worked"); });
}


// function addRow() {

// }

$(".updateList").on('submit', submitList);
// $(".updateList").on('return', addRow)