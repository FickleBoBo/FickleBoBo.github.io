import dict.EnglishDictionary;
import dict.KoreanDictionary;
import task.SpellCheckTaskV1;

public class DictionaryMainV1 {

    public static void main(String[] args) throws InterruptedException {
        // 영어 사전으로 맞춤법 검사기를 사용하는 스레드와 한국어 사전으로 맞춤법 검사기를 사용하는 스레드 생성
        Thread thread1 = new Thread(new SpellCheckTaskV1(new EnglishDictionary(), "app", "ag"), "영어 스레드");
        Thread thread2 = new Thread(new SpellCheckTaskV1(new KoreanDictionary(), "기린", "기무"), "한국어 스레드");

        // 영어 스레드 실행
        thread1.start();

        // 0.7초 대기
        Thread.sleep(700);

        // 한국어 스레드 실행
        thread2.start();

        // 출력 결과
        // 00:03:30.934 [   영어 스레드] word = app, isValid = true
        // 00:03:31.442 [   영어 스레드] typo = ag, suggestions = [] <- 대체 단어 조회에서 한국어 사전으로 변경돼서 조회 실패
        // 00:03:31.629 [  한국어 스레드] word = 기린, isValid = true
        // 00:03:31.946 [   영어 스레드] 종료
        // 00:03:32.135 [  한국어 스레드] typo = 기무, suggestions = [기러기, 기린, 기차]
        // 00:03:32.641 [  한국어 스레드] 종료
    }
}
