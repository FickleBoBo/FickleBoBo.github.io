package task;

import dict.Lexicon;
import dict.SpellCheckerUtil;

import java.util.List;

import static util.MyLogger.log;

// 맞춤법 검사기 작업으로 사용할 사전, 사전에 있는 단어인지 검색 작업, 대체 단어 검색 작업 수행
public class SpellCheckTaskV1 implements Runnable {

    private final Lexicon dictionary;
    private final String word;
    private final String typo;

    public SpellCheckTaskV1(Lexicon dictionary, String word, String typo) {
        this.dictionary = dictionary;
        this.word = word;
        this.typo = typo;
    }

    @Override
    public void run() {
        // 사전 세팅
        SpellCheckerUtil.setDictionary(dictionary);

        // 사전 세팅에 0.5초 걸린다고 가정
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }

        // 사전에 있는 단어인지 검색 작업
        boolean isValid = SpellCheckerUtil.isValid(word);
        log("word = " + word + ", isValid = " + isValid);

        // 사전에 있는 단어인지 검색 작업에 0.5초 걸린다고 가정
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }

        // 대체 단어 검색 작업
        List<String> suggestions = SpellCheckerUtil.suggestions(typo);
        log("typo = " + typo + ", suggestions = " + suggestions);

        // 대체 단어 검색 작업에 0.5초 걸린다고 가정
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }

        log("종료");
    }
}
