package dict;

import java.util.List;
import java.util.Set;

public class KoreanDictionary implements Lexicon {

    private final static Set<String> dictionary = Set.of("기차", "기러기", "기린", "감자");

    @Override
    public boolean isValid(String word) {
        return dictionary.contains(word);
    }

    @Override
    public List<String> getSuggestions(String typo) {
        if (isValid(typo)) return List.of();

        return dictionary.stream()
                .filter(word -> word.startsWith(String.valueOf(typo.charAt(0))))
                .toList();
    }
}
