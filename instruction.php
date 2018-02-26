<?php
//##################################################################
// Projekt IPP
// Autor: Jan Koci
// Datum: 26.2.2018
// Popis: Definice trid pro prvni cast projekt (parser.php)
//##################################################################

/**
 * Trida pro argument instrukce v IPPcode18
 * atribut $type    typ argumentu
 * atribut $value   hodnota argumentu
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
      $temp = explode('@', $argument);
      $this->value = strtoupper($temp[0]).'@'.$temp[1];
    }
    else if (preg_match('/^(int|string|bool)@.*/i', $argument))
    {
      $temp = explode('@', $argument);
      $temp[0] = strtolower($temp[0]);
      if ($temp[0] == "string")
      {
        $temp[1] = preg_replace('/&/', '&amp;', $temp[1]);
        $temp[1] = preg_replace(array('/</', '/>/'), array('&lt;', '&gt;'), $temp[1]);
      }
      else if ($temp[0] == "bool")
      {
        $temp[1] = strtolower($temp[1]); // true/false musi byt lowercase
      }
      $this->type = $temp[0];
      $this->value = $temp[1];
    }
    else
    {
      $argument = preg_replace('/&/', '&amp;', $argument);
      $argument = preg_replace(array('/</', '/>/'), array('&lt;', '&gt;'), $argument);
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
