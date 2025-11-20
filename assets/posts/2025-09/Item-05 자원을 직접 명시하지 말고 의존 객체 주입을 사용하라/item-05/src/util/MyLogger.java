package util;

import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

// 실행 시간, 스레드 이름, 파라미터를 출력하는 로거
public class MyLogger {

    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm:ss.SSS");

    private MyLogger() {
    }

    public static void log(Object obj) {
        String time = LocalTime.now().format(formatter);
        System.out.printf("%s [%9s] %s\n", time, Thread.currentThread().getName(), obj);
    }
}
