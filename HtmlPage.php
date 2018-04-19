<?php
  $page_html1 = "<!DOCTYPE html>
  <html>
    <head>
      <meta charset='utf-8'>
      <title>IPP project tests</title>
    </head>
    <style>
    body {
      font-family: 'lato', sans-serif;
    }
    .container {
      max-width: 600px;
      /* background: white; */
      border-radius:3px;
      border-collapse: collapse;
      padding:5px;
      width: 100%;
    }
    th {
      color:white;
      background:#1b1e23;
      border-right: 1px solid gray;
      font-size:24px;
      font-weight: 100;
      padding:24px;
      text-align:left;
    }

    /* th:first-child {
      border-top-left-radius:3px;
    } */

    /* th:last-child {
      border-top-right-radius:3px;
      border-right:none;
    } */

    tr {
      border-top: 1px solid #C1C3D1;
      border-bottom: 1px solid #C1C3D1;
      color:#1b1e24;
      font-size:16px;
      font-weight:normal;
      text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.1);
    }
    td {
      padding:20px;
      text-align:left;
      font-weight:300;
      font-size:18px;
      text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.1);
      border-right: 1px solid #C1C3D1;
    }

    .text_left {
      text-align: left;
    }

    .text_center {
      text-align: center;
    }

    .ok {
      background-color: #94b359;
    }

    .fail {
      background-color: #ed462f;
    }

    .button {
      background-color: #666B85;
      color: white;
      border: none;
      text-align: center;
      font-size: 16px;
      border-radius: 50%;
      padding: 7px 15px;
      display: block;
      margin: auto;
      box-shadow: 0 5px 5px rgba(0, 0, 0, 0.1);
    }

    h2 {
      font-size: 26px;
      margin: 20px 0;
      text-align: center;
    }
    </style>
    <body>
        <h2>IPP project test results:</h2>
          <table align='center' class='container'>
            <thead>
              <tr>
                <th class='text_left'>ID</th>
                <th class='text_left'>Test name</th>
                <th class='text_center'>Result</th>
                <th class='text_left'> </th>
              </tr>
            </thead>
            <tbody>
            ";

$page_html2 = "</tbody></table></body></html>";

?>
