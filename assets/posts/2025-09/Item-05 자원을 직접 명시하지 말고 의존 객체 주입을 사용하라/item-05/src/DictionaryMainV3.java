import dict.EnglishDictionary;
import dict.KoreanDictionary;
import task.SpellCheckTaskV3;

public class DictionaryMainV3 {

    public static void main(String[] args) throws InterruptedException {
        // 영어 사전으로 맞춤법 검사기를 사용하는 스레드와 한국어 사전으로 맞춤법 검사기를 사용하는 스레드 생성
        Thread thread1 = new Thread(new SpellCheckTaskV3(new EnglishDictionary(), "app", "ag"), "영어 스레드");
        Thread thread2 = new Thread(new SpellCheckTaskV3(new KoreanDictionary(), "기린", "기무"), "한국어 스레드");

        // 영어 스레드 실행
        thread1.start();

        // 0.7초 대기
        Thread.sleep(700);

        // 한국어 스레드 실행
        thread2.start();

        // 출력 결과
        // 00:42:05.509 [   영어 스레드] word = app, isValid = true
        // 00:42:06.018 [   영어 스레드] typo = ag, suggestions = [app, apple, audio]
        // 00:42:06.210 [  한국어 스레드] word = 기린, isValid = true
        // 00:42:06.520 [   영어 스레드] 종료
        // 00:42:06.717 [  한국어 스레드] typo = 기무, suggestions = [기차, 기린, 기러기]
        // 00:42:07.222 [  한국어 스레드] 종료
    }
}
