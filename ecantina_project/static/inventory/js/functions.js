$(document).ready(function(){

    $( "#slider-range-price" ).slider({
        range: true,
        min: 0,
        max: 500,
        values: [ 0, 100 ],
        slide: function( event, ui ) {
            $( "#price-amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
        }
    });
    $( "#price-amount" ).val( "$" + $( "#slider-range-price" ).slider( "values", 0 ) +
    " - $" + $( "#slider-range-price" ).slider( "values", 1 ) );

    $( "#slider-range-pl-price" ).slider({
        range: true,
        min: 0,
        max: 500,
        values: [ 0, 100 ],
        slide: function( event, ui ) {
            $( "#pl-price-amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
        }
    });
    $( "#pl-price-amount" ).val( "$" + $( "#slider-range-pl-price" ).slider( "values", 0 ) +
    " - $" + $( "#slider-range-pl-price" ).slider( "values", 1 ) );

    $('#advsearch-toggle').on('click', function(){
       if( $(this).find('span').hasClass('glyphicon-chevron-down') ){
           $('#inventory-search').slideDown();
           $(this).find('span').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
       }
        else{
           $('#inventory-search').slideUp();
           $(this).find('span').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
       }
    });

    $('#advsearch-pull-list-toggle').on('click', function(){
        if( $(this).find('span').hasClass('glyphicon-chevron-down') ){
            $('#inventory-pull-list-search').slideDown();
            $(this).find('span').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
        }
        else{
            $('#inventory-pull-list-search').slideUp();
            $(this).find('span').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
        }
    });

    $('.group-checkbox').on('click', function(){
        if( $(this).is(':checked') ){
            $(this).parentsUntil('.accordion').find('input[type=checkbox]').not('.group-checkbox').prop('checked',true);
        }
        else{
            $(this).parentsUntil('.accordion').find('input[type=checkbox]').not('.group-checkbox').prop('checked',false);
        }
    });

    $('body').on('click','.series-item',function(){
        $('.series-item').removeClass('selected');
        $(this).addClass('selected');
    });

    $( "#from" ).datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 1,
        onClose: function( selectedDate ) {
            $( "#to" ).datepicker( "option", "minDate", selectedDate );
        }
    });
    $( "#to" ).datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 1,
        onClose: function( selectedDate ) {
            $( "#from" ).datepicker( "option", "maxDate", selectedDate );
        }
    });

    $('.graph-type-menu .list-group-item').on('click',function(){
        $('.graph-type-menu .list-group-item').removeClass('active');
        $(this).addClass('active');
    });

    $('.orders-table tr').click(function(){
        $('.orders-table tr').removeClass('selected');
        $(this).addClass('selected');
    });

});

