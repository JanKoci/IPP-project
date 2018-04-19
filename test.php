<?php
//##################################################################
// Project IPP
// Author:  Jan Koci
// Date:    26.2.2018
// Brief:   Tests
//##################################################################


  include 'ArgParser.php';
  include 'HtmlPage.php';

  function create_file($file)
  {
    $myfile = fopen($file, "w") or die("Unable to open file!");
    fclose($myfile);
  }


  /**
   * TESTS
   */
  class Tests
  {
    public $tests;
    public $parse_script;
    public $int_script;

    function __construct($parse_script, $int_script)
    {
      $this->parse_script = $parse_script;
      $this->int_script = $int_script;
      $this->tests = array();
    }

    public function add_test($name)
    {
      if (array_key_exists($name, $this->tests))
      {
        fwrite(STDERR, "ERROR: 2 .src files cannot have the same name");
        exit(1);
      }
      $this->tests[$name] = 'ok';
    }

    public function run()
    {
      foreach ($this->tests as $test_name => $value) {
        $src_file = $test_name.".src";
        $in_file = $test_name.".in";
        $out_file = $test_name.".out";
        $rc_file = $test_name.".rc";
        $output = array();
        $return_val = 0;
        $xml_file = fopen("__out.xml", "w");
        $test_output = fopen("__test.out", "w");

        $rc_file_handle = fopen($rc_file, "r");
        $return_val_expected = (int)fread($rc_file_handle, 2);
        fclose($rc_file_handle);
        exec("chmod +x {$this->parse_script}");
        exec("php {$this->parse_script} < {$src_file}", $output, $return_val);

        if ($return_val != 0)
        {
          fclose($xml_file);
          echo "parse.php failed with exit code {$return_val}", "\n";
          if ($return_val != $return_val_expected)
          {
            $this->tests[$test_name] = 'fail';
          }
          continue;
        }

        foreach ($output as $line) {
          fwrite($xml_file, $line."\n");
        }
        fclose($xml_file);
        $output = array();
        exec("chmod +x {$this->int_script}");
        exec("python {$this->int_script} --source __out.xml < {$in_file}", $output, $return_val);
        foreach ($output as $line) {
          fwrite($test_output, $line."\n");
        }
        fclose($test_output);
        if ($return_val != $return_val_expected)
        {
          echo "interpret.py failed with exit code {$return_val}", "\n";
          $this->tests[$test_name] = 'fail';
        }
        else
        {
          $output = array();
          exec("diff __test.out {$out_file}", $output);
          if (!empty($output))
          {
            $this->tests[$test_name] = 'fail';
            echo "interpret.py output not same", "\n";
          }
        }
      }
      exec("rm __out.xml __test.out");
      print_r($this->tests);
    }
    public function generate_HTML()
    {
      global $page_html1;
      global $page_html2;
      $page_html = $page_html1;
      $i = 1;
      foreach ($this->tests as $test_name => $value) {
        $page_html .= "<tr class='{$value}'>
                        <td class='text_left'>{$i}</td>
                        <td class='text_left'>{$test_name}</td>
                        <td class='text_center'>{$value}</td>
                        <td><button type='button' class='button'>?</button></td>
                      </tr>";
        $i += 1;
      }
      $page_html .= $page_html2;
      file_put_contents("index.html", $page_html);
    }
  }

  $message = "USAGE: php test.php [--directory=path] [--help] [--recursive] [--pase-script=file]";
  $message .= " [--int-script=file]";
  $parser = new ArgParser($usage=$message);
  $parser->add_argument("-help", $help="print this help message", $action='print_help');
  $parser->add_argument("-directory", $help="directory with the tests", $action='get_val');
  $parser->add_argument("-recursive", $help="search for tests recursively", $action='store_true');
  $parser->add_argument("-parse-script", $help="file with IPPcode18 parser", $action='get_val');
  $parser->add_argument("-int-script", $help="file with IPPcode18 interpreter", $action='get_val');

  $args = $parser->parse();

  if (!$args['parsescript'])
  {
    $args['parsescript'] = 'parse.php';
  }
  if (!$args['intscript'])
  {
    $args['intscript'] = 'interpret.py';
  }
  if (!$args['directory'])
  {
    $args['directory'] = '.';
  }

  if (!file_exists($args['directory']))
  {
    fwrite(STDERR, "ERROR, directory does not exist\n");
    exit(1);
  }
  if (!file_exists($args['parsescript']))
  {
    fwrite(STDERR, "ERROR, file {$args['parsescript']} does not exist\n");
    exit(1);
  }
  if (!file_exists($args['intscript']))
  {
    fwrite(STDERR, "ERROR, file {$args['intscript']} does not exist\n");
    exit(1);
  }
  print_r($args);

  if ($args['recursive'])
  {
    $dir_iterator = new RecursiveDirectoryIterator($args['directory']);
    $iterator = new RecursiveIteratorIterator($dir_iterator, RecursiveIteratorIterator::SELF_FIRST);
    $src_files = array();
    $in_files = array();
    $out_files = array();
    $rc_files = array();

    foreach ($iterator as $file) {
      // $name = $file->getFilename();
      // echo $name, "\n";
      if (preg_match('/^.+\.src$/', $file->getPathname()))
      {
        array_push($src_files, $file->getPathname());
      }
      else if (preg_match('/^.+\.in$/', $file->getPathname()))
      {
        array_push($in_files, $file->getPathname());
      }
      else if (preg_match('/^.+\.out$/', $file->getPathname()))
      {
        array_push($out_files, $file->getPathname());
      }
      else if (preg_match('/^.+\.rc$/', $file->getPathname()))
      {
        array_push($rc_files, $file->getPathname());
      }
    }

    // debug:
    // print_r($src_files);
    // print_r($in_files);
    // print_r($out_files);
    // print_r($rc_files);
  }
  else
  {
    if ($args['directory'][-1] != '/')
    {
      $args['directory'] .= '/';
    }
    $src_files = glob($args['directory']."*.src");
    $in_files = glob($args['directory']."*.in");
    $out_files = glob($args['directory']."*.out");
    $rc_files = glob($args['directory']."*.rc");
  }

  $tests = new Tests($args['parsescript'], $args['intscript']);
  foreach ($src_files as $file) {
    $file_name = explode('.', $file)[0];
    if (!in_array($file_name.".in", $in_files))
    {
      create_file($file_name.".in");
    }
    if (!in_array($file_name.".out", $out_files))
    {
      create_file($file_name.".out");
    }
    if (!in_array($file_name.".rc", $rc_files))
    {
      create_file($file_name.".rc");
      file_put_contents($file_name.".rc", "0");
    }
    $tests->add_test($file_name);
  }

  // run all tests
  $tests->run();
  $tests->generate_HTML();


?>
