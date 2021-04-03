function fnExcelReport()
{
    var tab_text="<table border='2px'>";
    var textRange; var j=0;
    tab = document.getElementById('table-id'); // id of table
    tab_text = tab_text + '<h2 style="text-align:center"> Thống kê</h2>';
    tab_text = tab_text + "<tr style='background-color:#87AFC6'>";
    for(j = 0 ; j < tab.rows.length ; j++)
    {
        tab_text=tab_text+tab.rows[j].innerHTML+"</tr>";
        //tab_text=tab_text+"</tr>";
    }
    tab_text=tab_text+"</table>";
    var x = tab.rows.length -1;
    tab_text = tab_text + '<h4> Tổng số cây: '+x+'</h4>';
    tab_text= tab_text.replace(/<A[^>]*>|<\/A>/g, "");//remove if u want links in your table
    tab_text= tab_text.replace(/<img[^>]*>/gi,""); // remove if u want images in your table
    tab_text= tab_text.replace(/<input[^>]*>|<\/input>/gi, ""); // reomves input params

    var ua = window.navigator.userAgent;
    var msie = ua.indexOf("MSIE ");

    if (msie > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./))      // If Internet Explorer
    {
        txtArea1.document.open("txt/html","replace");
        txtArea1.document.write(tab_text);
        txtArea1.document.close();
        txtArea1.focus();
        sa=txtArea1.document.execCommand("SaveAs",true,"Say Thanks to Sumit.xlsx");
    }
   else {//other browser not tested on IE 11
        // sa = window.open('data:application/vnd.ms-excel,' + encodeURIComponent(tab_text));
        // sa.document.title = "your new title";

        //new added by amit
     let a = $("<a />", {
             href: 'data:application/vnd.ms-excel,' + encodeURIComponent(tab_text),
             download: "Thống-kê.xls"
         })
         .appendTo("body")
         .get(0)
         .click();
         e.preventDefault();
     }

     return (sa);
 }
