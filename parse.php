<?php
//##################################################################
// Project IPP
// Author:  Jan Koci
// Date:    26.2.2018
// Brief:   Parser vstupniho kodu v IPPcode18
//    Provede lexikalni a syntaktickou analyzu kodu, ze standartniho
//    vstupu a prevede jej do XML reprezentace
//##################################################################
  include 'instruction.php';
  include 'my_regex.php';
  include 'ArgParser.php';

  // parse command line arguments
  $message = "USAGE: php parse.php [--help] [--stats=file [--comments] [--loc]]";
  $parser = new ArgParser($usage=$message);
  $parser->add_argument("-help", $help='print this help message', $action='print_help');
  $parser->add_argument("-stats", $help='generate statistics about parsed code in IPPcode18',
                                  $action='get_val');
  $parser->add_argument("-comments", $help='count number of comments in code, can be used only with --stats argument',
                                     $action='store_true');
  $parser->add_argument("-loc", $help='count number of instructions in code, can be used only with --stats argument',
                                      $action='store_true');
  $args = $parser->parse();

  if ($args['loc'] || $args['comments']) {
    if (!$args['stats']) {
      print("ERROR: arguments --loc and --comments cannot be used without argument --stats=filename\n");
      exit(10);
    }
  }
  if ($args['stats']) {
    $stats_file = fopen($args['stats'], "w") or die("ERROR: unable to open file\n");
  }


  // array of all instructions
  $instructions_array = array();
  $comments = 0; // count number of comments
  $numof_insts = 0;

  // na zacatku musi byt .ippcode18
  do {
    $line = fgets(STDIN);
    $data = explode('\n', $line);
    $data = explode('#', $data[0]);
    if ($data[1]) {$comments++;}
    $data = preg_split("/\s+/", $data[0], -1, PREG_SPLIT_NO_EMPTY);
  } while (!$data);

  if (strtolower($data[0]) != ".ippcode18")
  {
    fwrite(STDERR, "ERROR: Kod musi zacinat nazvem .ippcode18");
  }

  while ($line = fgets(STDIN)) {
    // splits line into words, ignores comments (starting with '#')
    $data = explode('\n', $line);
    $data = explode('#', $data[0]);
    if ($data[1]) {$comments++;}
    $data = preg_split("/\s+/", $data[0], -1, PREG_SPLIT_NO_EMPTY);

    if ($data)
    {
      switch (strtolower($data[0])) {
    // ______ <var> <symb> ______
        case "move":
        case "int2char":
        case "strlen":
        case "type":
            // check correct number of arguments
            if (count($data) != 3)
            {
              fwrite(STDERR, "ERROR: Instrukce '$data[0]' ocekava argumenty <var> a <symb>\n");
              exit(21);
            }
            //  <var>
            if (!preg_match($var_regexp, $data[1]))
            {
              fwrite(STDERR, "ERROR: Argument '$data[1]' u instrukce '$data[0]' musi byt typu <var>\n");
              exit(21);
            }
            // <symb>
            if (!preg_match($symb_regexp, $data[2]))
            {
              fwrite(STDERR, "ERROR: Argument '$data[2]' u instrukce '$data[0]' musi byt typu <symb>\n");
              exit(21);
            }

            $instruction = new Instruction($data);
            array_push($instructions_array, $instruction);

        break;

    // ______ no argument ______
        case "createframe":
        case "pushframe":
        case "popframe":
        case "return":
        case "break":
          if (count($data) != 1)
          {
            fwrite(STDERR, "ERROR: Instrukce '$data[0]' musi byt bez argumentu\n");
            exit(21);
          }
          $instruction = new Instruction($data);
          array_push($instructions_array, $instruction);

        break;

    // ______ <var> ______
        case "defvar":
        case "pops":
          if (count($data) != 2)
          {
            fwrite(STDERR, "ERROR: Instrukce '$data[0]' ocekava jeden argument <var>\n");
            exit(21);
          }
          if (!preg_match($var_regexp, $data[1]))
          {
            fwrite(STDERR, "ERROR: Argument '$data[1]' u instrukce '$data[0]' musi byt typu <var>\n");
            exit(21);
          }
          $instruction = new Instruction($data);
          array_push($instructions_array, $instruction);

        break;

    // ______ <label> ______
        case "call":
        case "label":
        case "jump":
          if (count($data) != 2)
          {
            fwrite(STDERR, "ERROR: Instrukce '$data[0]' ocekava jeden argument <label>\n");
            exit(21);
          }
          if (!preg_match($label_regexp, $data[1]))
          {
            fwrite(STDERR, "ERROR: Argument '$data[1]' u instrukce '$data[0]' musi byt typu <label>\n");
            exit(21);
          }
          $instruction = new Instruction($data);
          array_push($instructions_array, $instruction);

        break;

    // ______ <symb> ______
        case "pushs":
        case "write":
        case "dprint":
          if (count($data) != 2)
          {
            fwrite(STDERR, "ERROR: Instrukce '$data[0]' ocekava jeden argument <symb>\n");
            exit(21);
          }
          if (!preg_match($symb_regexp, $data[1]))
          {
            fwrite(STDERR, "ERROR: Argument '$data[1]' u instrukce '$data[0]' musi byt typu <symb>\n");
            exit(21);
          }
          $instruction = new Instruction($data);
          array_push($instructions_array, $instruction);
        break;

    // ______ <var> <symb1> <symb2> ______
        case "add":
        case "sub":
        case "mul":
        case "idiv":
        case "lt":
        case "gt":
        case "eq":
        case "and":
        case "or":
        case "not":
        case "stri2int":
        case "concat":
        case "getchar":
        case "setchar":
          if (count($data) != 4)
          {
            fwrite(STDERR, "ERROR: Instrukce '$data[0]' ocekava tri argumenty:
                            <var> <symb1> <symb2>\n");
            exit(21);
          }
          // <var>
          if (!preg_match($var_regexp, $data[1]))
          {
            fwrite(STDERR, "ERROR: Argument '$data[1]' u instrukce '$data[0]' musi byt typu <var>\n");
            exit(21);
          }
          // <symb1>
          if (!preg_match($symb_regexp, $data[2]))
          {
            fwrite(STDERR, "ERROR: Argument '$data[2]' u instrukce '$data[0]' musi byt typu <symb>\n");
            exit(21);
          }
          // <symb2>
          if (!preg_match($symb_regexp, $data[3]))
          {
            fwrite(STDERR, "ERROR: Argument '$data[3]' u instrukce '$data[0]' musi byt typu <symb>\n");
            exit(21);
          }
          $instruction = new Instruction($data);
          array_push($instructions_array, $instruction);
        break;

    // ______ <var> <type> ______
        case "read":
          if (count($data) != 3)
          {
            fwrite(STDERR, "ERROR: Instrukce '$data[0]' ocekava argumenty <var> a <type>\n");
            exit(21);
          }
          // <var>
          if (!preg_match($var_regexp, $data[1]))
          {
            fwrite(STDERR, "ERROR: Argument '$data[1]' u instrukce '$data[0]' musi byt typu <var>\n");
            exit(21);
          }
          // <type>
          if (!preg_match($type_regexp, $data[2]))
          {
            fwrite(STDERR, "ERROR: Argument '$data[2]' u instrukce '$data[0]' musi byt typu <type>\n");
            exit(21);
          }
          $instruction = new Instruction($data);
          // only in case the instruction is of type 'type', it has to be
          // set up manually
          $instruction->getArguments()[1]->type = "type";
          $instruction->getArguments()[1]->value = strtolower($data[2]);
          array_push($instructions_array, $instruction);
        break;

    //_______ <label> <symb1> <symb2> ______
        case "jumpifeq":
        case "jumpifneq":
          if (count($data) != 4)
          {
            fwrite(STDERR, "ERROR: Instrukce '$data[0]' ocekava tri argumenty:
                            <label> <symb1> <symb2>\n");
            exit(21);
          }
          // <label>
          if (!preg_match($label_regexp, $data[1]))
          {
            fwrite(STDERR, "ERROR: Argument '$data[1]' u instrukce '$data[0]' musi byt typu <label>\n");
            exit(21);
          }
          // <symb1>
          if (!preg_match($symb_regexp, $data[2]))
          {
            fwrite(STDERR, "ERROR: Argument '$data[2]' u instrukce '$data[0]' musi byt typu <symb>\n");
            exit(21);
          }
          // <symb2>
          if (!preg_match($symb_regexp, $data[3]))
          {
            fwrite(STDERR, "ERROR: Argument '$data[3]' u instrukce '$data[0]' musi byt typu <symb>\n");
            exit(21);
          }
          $instruction = new Instruction($data);
          array_push($instructions_array, $instruction);
        break;

        // unknown instruction
        default:
          fwrite(STDERR, "ERROR: Unknown instruction '$data[0]'\n");
          exit(21);
        break;
      }
    }
  }

  // number of instructions for statistics
  $numof_insts = count($instructions_array);

  // ______ generates XML representation of the code _______
  $xml = new DOMDocument('1.0', 'UTF-8');
  $program = $xml->createElement('program');
  $program->setAttribute("language", "IPPcode18");
  $xml->appendChild($program);

  $counter = 1;
  $arg_counter;
  foreach ($instructions_array as $instruction) {
    $arg_counter = 1;
    $xml_inst = $xml->createElement('instruction');
    $xml_inst->setAttribute("order", $counter);
    $xml_inst->setAttribute("opcode", $instruction->getType());
    foreach (array_values($instruction->getArguments()) as $i => $arg) {
      $xml_arg = $xml->createElement("arg{$arg_counter}", $arg->getValue());
      $xml_arg->setAttribute("type", $arg->getType());
      $xml_inst->appendChild($xml_arg);
      $arg_counter++;
    }
    $program->appendChild($xml_inst);
    $counter++;
  }

  $xml->formatOutput = true;
  print $xml->saveXML();

  // write the statistics if needed
  if ($args['stats']) {
    if ($args['comments']) {
      fwrite($stats_file, "Number of comments: \t'$comments'\n");
    }
    if ($args['loc']) {
      fwrite($stats_file, "Number of instructions:\t'$numof_insts'\n");
    }
    fclose($stats_file);
  }

?>
