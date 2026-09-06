-- Render inline code as \texttt with break opportunities after separators, so that long
-- repository paths wrap inside the text block instead of running off the page.
local function escape(s)
  s = s:gsub("\\", "\1")
  s = s:gsub("([{}$&#_%%^~])", "\\%1")
  s = s:gsub("\1", "\\textbackslash{}")
  s = s:gsub("\\%^", "\\^{}")
  s = s:gsub("\\~", "\\~{}")
  return s
end

function Code(el)
  local s = escape(el.text)
  s = s:gsub("/", "/\\allowbreak{}")
  s = s:gsub("%.", ".\\allowbreak{}")
  s = s:gsub("%-", "-\\allowbreak{}")
  s = s:gsub(":", ":\\allowbreak{}")
  s = s:gsub("\\_", "\\_\\allowbreak{}")
  return pandoc.RawInline("latex", "\\texttt{" .. s .. "}")
end
