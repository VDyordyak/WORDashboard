$("#all_users").click(function () {
    var checkboxes = document.getElementsByName('assigned_user');
    // loop over them all
    if (checkboxes[0].checked == true == true){
        for (var i=0; i<checkboxes.length; i++) {
            checkboxes[i].checked = false;
        }
    }
    else{
        for (var i=0; i<checkboxes.length; i++) {
            checkboxes[i].checked = true;
        }
    }
});
$(".show-more").click(function () {
    var elements = $(".hiden");
    $.each(elements, function (index, tr) {
        $(this).css("display", "table-row");
    });
    $(this).css("display", "none");
});

$(".checkbox-dropdown").click(function () {
    $(this).toggleClass("is-active");
});

$(".checkbox-dropdown ul").click(function(e) {
    e.stopPropagation();
});
function getCheckedBoxes(chkboxName) {
    var checkboxes = document.getElementsByName(chkboxName);
    var checkboxesChecked = [];
    // loop over them all
    for (var i=0; i<checkboxes.length; i++) {
        // And stick the checked ones onto an array...
        if (checkboxes[i].checked) {
            if (checkboxes[i].value != "all"){
                checkboxesChecked.push(checkboxes[i].value);
            }
        }
    }
    // Return the array if it is non-empty, or null
    return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}
function getUncheckedBoxes(chkboxName) {
    var checkboxes = document.getElementsByName(chkboxName);
    var checkboxesChecked = [];
    // loop over them all
    for (var i=0; i<checkboxes.length; i++) {
        // And stick the checked ones onto an array...
        if (checkboxes[i].checked == false) {
            checkboxesChecked.push(checkboxes[i].value);
        }
    }
    // Return the array if it is non-empty, or null
    return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}