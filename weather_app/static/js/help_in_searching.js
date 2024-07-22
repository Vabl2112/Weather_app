
            var token = "e54f6ea734ae60d06ed508c9579994877cb58dc8";
            var $city = $("#city");

            function removeNonCity(suggestions) {
              return suggestions.filter(function(suggestion) {
                return suggestion.data.fias_level !== "65";
              });
            }

            function join(arr /*, separator */) {
              var separator = arguments.length > 1 ? arguments[1] : ", ";
              return arr.filter(function(n){return n}).join(separator);
            }

            function cityToString(address) {
              return join([
                  join([address.city_type, address.city], " "),
                  join([address.settlement_type, address.settlement], " ")
                ]);
            }

            // Ограничиваем область поиска от города до населенного пункта
            $city.suggestions({
              token: token,
              type: "ADDRESS",
              hint: false,
              count: 20,
              geoLocation: false,
              bounds: "city-settlement",
              onSuggestionsFetch: removeNonCity
            });
