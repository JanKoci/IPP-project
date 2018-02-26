<?php
//##################################################################
// Project IPP
// Author: Jan Koci
// Date: 26.2.2018
// Brief: Regular expressions for parsing the IPPcode18 language
//##################################################################

$int_regexp = '/^int@[-+]?(\d)+$/i';
$bool_regexp = '/^bool@(true|false)$/i';
$string_regexp = '/^string@[^\s#]*$/i';
// $symb_regexp ... ($int_regexp)|($bool_regexp)|($string_regexp)|($var_regexp)
$symb_regexp = "/(^int@[-+]?(\d)+$)|(^bool@(true|false)$)|(^string@[^\s#]*$)|(^(gf|lf|tf)@[a-zA-Z_\-&%\*\$]+[[:alnum:]_\-&%\*\$]*$)/i";
$var_regexp = '/^(gf|lf|tf)@[a-zA-Z_\-&%\*\$]+[[:alnum:]_\-&%\*\$]*$/i';
$label_regexp = '/^[a-zA-Z_\-&%\*\$]+[[:alnum:]_\-&%\*\$]*$/i';
$type_regexp = '/^(int|string|bool)$/i';
?>
