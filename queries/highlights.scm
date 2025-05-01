(binnary_expression
  (_)
  "."
  (_) @variable.other.member) ; @function.method

(const_string) @string
(const_number) @number
(at_operator) @keyword
(unary_expression) @function.builtin

["(" ")" "[" "]" "{" "}"]  @punctuation.bracket

["."] @punctuation.delimiter

; ["$"] @punctuation.special

(comment) @comment
