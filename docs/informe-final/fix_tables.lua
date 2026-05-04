-- Pandoc Lua filter: assign equal explicit column widths to tables that
-- have ColWidthDefault (pipe tables). This forces LaTeX to use p{} column
-- specifiers, enabling text wrapping and preventing horizontal overflow.
function Table(t)
  local n = #t.colspecs
  if n == 0 then return t end

  -- Only fix tables where ALL columns have default (auto) width,
  -- i.e., pipe tables. Leave grid/multiline tables unchanged.
  local all_default = true
  for _, spec in ipairs(t.colspecs) do
    if type(spec[2]) == 'number' then
      all_default = false
      break
    end
  end

  if all_default then
    for i, spec in ipairs(t.colspecs) do
      spec[2] = 1.0 / n
    end
  end

  return t
end
