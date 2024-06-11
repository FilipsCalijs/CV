<?php

function determinant(array $matrix): int {
  $rows = count($matrix);
  
  if ($rows === 1) {
    return $matrix[0][0];
  }

  $determinant = 0;
  // Loop through elements in the first row
  for ($col = 0; $col < $rows; $col++) {
    $minor = createMinor($matrix, 0, $col);
    $determinant += pow(-1, $col) * $matrix[0][$col] * determinant($minor);
  }

  return $determinant;
}

function createMinor($matrix, $row, $col) {
  $minor = [];
  for ($i = 0; $i < count($matrix); $i++) {
    if ($i === $row) {
      continue;
    }
    $newRow = [];
    for ($j = 0; $j < count($matrix[$i]); $j++) {
      if ($j === $col) {
        continue;
      }
      $newRow[] = $matrix[$i][$j];
    }
    $minor[] = $newRow;
  }
  return $minor;
}

// made with AI, i can't understand taks