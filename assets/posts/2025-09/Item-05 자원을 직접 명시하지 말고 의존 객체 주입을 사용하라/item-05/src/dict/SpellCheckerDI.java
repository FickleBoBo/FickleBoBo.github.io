package dict;

import java.util.List;

public class SpellCheckerDI {

    private final Lexicon dictionary;

    public SpellCheckerDI(Lexicon dictionary) {
        this.dictionary = dictionary;  // NPE 방지까지 하면 굿
    }

    public boolean isValid(String word) {
        return dictionary.isValid(word);
    }

    public List<String> suggestions(String typo) {
        return dictionary.getSuggestions(typo);
    }
}
