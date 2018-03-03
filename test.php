<?php
//##################################################################
// Project IPP
// Author:  Jan Koci
// Date:    26.2.2018
// Brief:   Tests
//##################################################################

  include 'ArgParser.php';

  $message = "USAGE: php test.php [--directory=path] [--help] [--recursive] [--pase-script=file]";
  $message .= " [--int-script=file]";
  $parser = new ArgParser($usage=$message);
  $parser->add_argument("-help", $help="print this help message", $action='print_help');
  $parser->add_argument("-directory", $help="directory with the tests", $action='get_val');
  $parser->add_argument("-recursive", $help="search for tests recursively", $action='store_true');
  $parser->add_argument("-parse-script", $help="file with IPPcode18 parser", $action='get_val');
  $parser->add_argument("-int-script", $help="file with IPPcode18 interpreter", $action='get_val');

  $args = $parser->parse();

  print_r($args);


?>
