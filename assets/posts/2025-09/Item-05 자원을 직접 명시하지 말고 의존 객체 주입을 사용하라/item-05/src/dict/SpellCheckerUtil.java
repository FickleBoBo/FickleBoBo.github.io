package dict;

import java.util.List;

public class SpellCheckerUtil {

    private static Lexicon dictionary = new EnglishDictionary();

    private SpellCheckerUtil() {
    }

    public static boolean isValid(String word) {
        return dictionary.isValid(word);
    }

    public static List<String> suggestions(String typo) {
        return dictionary.getSuggestions(typo);
    }

    // 사전을 변경할 수 있는 메서드 제공으로 유연성을 높일 시 동기화 문제 발생 가능
    public static void setDictionary(Lexicon dictionary) {
        SpellCheckerUtil.dictionary = dictionary;
    }
}
