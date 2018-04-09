<?php
//##################################################################
// Project IPP
// Author: Jan Koci
// Date: 26.2.2018
// Brief: Class definitions for parse.php
//##################################################################

/**
 * Class for instruction's argument in ippcode18
 * attribute $type    type of argument
 * attribute $value   value of argument
 */
class Argument
{
  public $type;
  public $value;

  function __construct($argument)
  {
    if (preg_match('/^(lf|gf|tf)@.*/i', $argument))
    {
      $this->type = 'var';
      $temp = explode('@', $argument, 2);
      $this->value = strtoupper($temp[0]).'@'.$temp[1];
    }
    else if (preg_match('/^(int|string|bool)@.*/i', $argument))
    {
      $temp = explode('@', $argument, 2);
      $temp[0] = strtolower($temp[0]);

      if ($temp[0] == "bool")
      {
        $temp[1] = strtolower($temp[1]); // true/false must be lowercase
      }
      $this->type = $temp[0];
      $this->value = $temp[1];
    }
    else
    {

      $this->type = 'label';
      $this->value = $argument;
    }
  }

  public function getType()
  {
    return $this->type;
  }

  public function getValue()
  {
    return $this->value;
  }
}

  /**
   * Class representing instruction in IPPcode18 language
   * attribute $type        type (=name) of the instruction
   * attribute $arguments   array of Argument objects
   */
  class Instruction
  {
    private $type;
    private $arguments = array();

    function __construct($data)
    {
      $this->type = strtoupper($data[0]);
      for ($i = 1; $i < count($data); $i++)
      {
        $argument = new Argument($data[$i]);
        array_push($this->arguments, $argument);
      }

    }

    public function getType()
    {
      return $this->type;
    }

    public function getArguments()
    {
      return $this->arguments;
    }

    public function getArgsCount()
    {
      return count($this->arguments);
    }

  }

  // ------ USAGE ------
  // $data = ["mOve", "iNt@-2", "INT", "BOOL@TruE", "StRinG@var1<var2&>var3", "Integer"];
  // $instruction = new Instruction($data);
  // $instruction->getArguments()[1]->type = "type";
  // $instruction->getArguments()[1]->value = strtolower($data[2]);
  // print_r($instruction);
 ?>
