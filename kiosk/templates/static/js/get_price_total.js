$(document).ready(function() {
    sum = 0.00
    $(".selection_price").each(function() {
        result = $(this).html().substring(1, $(this).html().length);
        if (parseFloat(result, 10)) {
            sum += parseFloat(result, 10);
        } else {
            console.log(typeof(result));
        }
    });
    $("#price_total").html("$" + sum.toFixed(2));
});
