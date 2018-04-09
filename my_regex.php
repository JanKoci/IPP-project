<?php
//##################################################################
// Project IPP
// Author: Jan Koci
// Date: 26.2.2018
// Brief: Regular expressions for parsing the IPPcode18 language
//##################################################################

$int_regexp = '/^int@[-+]?(\d)+$/';
$bool_regexp = '/^bool@(true|false)$/';
$string_regexp = '/^string@[^\s#]*$/';
$symb_regexp = "/(^int@[-+]?(\d)+$)|(^bool@(true|false)$)|(^string@[^\s#]*$)|(^(GF|LF|TF)@[a-zA-Z_\-&%\*\$]+[[:alnum:]_\-&%\*\$]*$)/";
$var_regexp = '/^(GF|LF|TF)@[a-zA-Z_\-&%\*\$]+[[:alnum:]_\-&%\*\$]*$/';
$label_regexp = '/^[a-zA-Z_\-&%\*\$]+[[:alnum:]_\-&%\*\$]*$/';
$type_regexp = '/^(int|string|bool)$/';
?>
