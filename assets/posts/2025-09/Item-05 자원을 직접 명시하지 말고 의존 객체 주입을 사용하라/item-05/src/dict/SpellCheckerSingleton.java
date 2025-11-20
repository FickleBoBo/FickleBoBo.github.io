package dict;

import java.util.List;

public class SpellCheckerSingleton {

    private Lexicon dictionary = new EnglishDictionary();

    // 싱글톤 파트
    private static final SpellCheckerSingleton INSTANCE = new SpellCheckerSingleton();

    private SpellCheckerSingleton() {
    }

    public static SpellCheckerSingleton getInstance() {
        return INSTANCE;
    }
    // 싱글톤 파트

    public boolean isValid(String word) {
        return dictionary.isValid(word);
    }

    public List<String> suggestions(String typo) {
        return dictionary.getSuggestions(typo);
    }

    // 사전을 변경할 수 있는 메서드 제공으로 유연성을 높일 시 동기화 문제 발생 가능
    public void setDictionary(Lexicon dictionary) {
        this.dictionary = dictionary;
    }
}
