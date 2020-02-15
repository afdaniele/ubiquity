String::format = (args...) ->
  @replace /{(\d+)}/g, (match, number) ->
    if number < args.length then args[number] else match

