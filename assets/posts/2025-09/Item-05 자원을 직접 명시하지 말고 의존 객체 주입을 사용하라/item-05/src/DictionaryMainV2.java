import dict.EnglishDictionary;
import dict.KoreanDictionary;
import task.SpellCheckTaskV2;

public class DictionaryMainV2 {

    public static void main(String[] args) throws InterruptedException {
        // 영어 사전으로 맞춤법 검사기를 사용하는 스레드와 한국어 사전으로 맞춤법 검사기를 사용하는 스레드 생성
        Thread thread1 = new Thread(new SpellCheckTaskV2(new EnglishDictionary(), "app", "ag"), "영어 스레드");
        Thread thread2 = new Thread(new SpellCheckTaskV2(new KoreanDictionary(), "기린", "기무"), "한국어 스레드");

        // 영어 스레드 실행
        thread1.start();

        // 0.7초 대기
        Thread.sleep(700);

        // 한국어 스레드 실행
        thread2.start();

        // 출력 결과
        // 00:07:47.886 [   영어 스레드] word = app, isValid = true
        // 00:07:48.394 [   영어 스레드] typo = ag, suggestions = [] <- 대체 단어 조회에서 한국어 사전으로 변경돼서 조회 실패
        // 00:07:48.579 [  한국어 스레드] word = 기린, isValid = true
        // 00:07:48.900 [   영어 스레드] 종료
        // 00:07:49.082 [  한국어 스레드] typo = 기무, suggestions = [기러기, 기린, 기차]
        // 00:07:49.586 [  한국어 스레드] 종료
    }
}
