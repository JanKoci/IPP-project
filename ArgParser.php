<?php

/**
 * Argument parser for php
 */
class ArgParse
{
  public $arguments;
  private $arg_vec;

  function __construct()
  {
    global $argv;
    $this->argumets = array();
    $this->arg_vec = $argv;
  }

  public function add_argument($name, $help='', $action='get_val')
  {
    if ($action == "get_val") {
      $regex = '/^-?'.$name.'(=[^\s]*)?$/';
    }
    else {
      $regex = '/^-?'.$name.'$/';
    }
    $argument = new Arg($name, $help, $action, $regex);
    array_push($this->argumets, $argument);
  }

  public function parse()
  {
    $ret_args = array();
    foreach ($this->argumets as $arg) {
      // find matches in argv
      $match = preg_grep($arg->regex, $this->arg_vec);
      if ($match) {
        $index = array_keys($match);
        if (count($index) > 1) {
          print("ERROR: argument '$arg->name' cannot be used more than once\n");
          exit(10);
        }
        $index = $index[0];
        switch ($arg->action) {
          case 'store_true':
            // remove the first --
            $ret_args[$arg->name] = 'true';
            unset($this->arg_vec[$index]);
            break;
          case 'store_false':
            // remove the first --
            $ret_args[$arg->name] = 'false';
            unset($this->arg_vec[$index]);
            break;

          case 'get_val':
            // remove the first --
            $data = explode('=', $match[$index]);
            if (count($data) == 1) {
              $value = $this->arg_vec[$index+1];
              unset($this->arg_vec[$index+1]);
            }
            else {
              $value = $data[1];
            }
            $ret_args[$arg->name] = $value;
            unset($this->arg_vec[$index]);
            break;
        }
      }
    }
    if (count($this->arg_vec) != 1) {
      print("ERROR: unknown arguments\n");
      exit(10);
    }
    return $ret_args;
  }

}

/**
 *
 */
class Arg
{
  public $name;
  public $help;
  public $action;
  public $regex;

  function __construct($name, $help, $action, $regex)
  {
    $this->name = $name;
    $this->help = $help;
    $this->action = $action;
    $this->regex = $regex;
  }
}

  $parser = new ArgParse();
  $parser->add_argument('-source', $help="source filename", $action='get_val');
  $parser->add_argument("-help", $help="print help message", $action='store_true');
  // print_r($parser);
  $args = $parser->parse();
  print_r($args);



?>
