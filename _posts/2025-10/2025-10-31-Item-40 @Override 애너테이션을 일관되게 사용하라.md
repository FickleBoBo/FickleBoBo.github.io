---
title: "[Item-40] @Override 애너테이션을 일관되게 사용하라"
date: 2025-10-31
categories: [Java, Effective Java 3/E]
tags: [Effective Java 3/E]
toc: true
math: true
image: /assets/posts/2025-10/Item-40%20@Override%20애너테이션을%20일관되게%20사용하라/thumbnail.jpg
---

## 핵심 정리

상위 클래스의 메서드를 재정의하려는 모든 메서드에 @Override 애너테이션을 달자. 예외는 구체 클래스에서 상위 클래스의 추상 메서드를 재정의할 경우 단 하나 뿐이다.(단다고 문제될 것도 없다.)

---

## @Override 애너테이션

Java가 기본으로 제공하는 애너테이션 중 보통의 프로그래머에게 가장 중요한 것은 @Override일 것이다. @Override는 메서드 선언에만 달 수 있으며, 이 애너테이션이 달렸다는 것은 상위 타입의 메서드를 재정의했음을 뜻한다.

아래는 @Override 애너테이션 코드로 `@Target(ElementType.METHOD)`를 통해 메서드에만 적용가능한 것과 `@Retention(RetentionPolicy.SOURCE)`를 통해 소스 코드에만 존재하고, 컴파일 후(자바 바이트 코드) 사라지는 것을 알 수 있다.

![](/assets/posts/2025-10/Item-40%20@Override%20애너테이션을%20일관되게%20사용하라/assets/photo1.png)

@Override 애너테이션을 달 경우 잘못된 오버라이딩에 대해 컴파일 단계에서 오류를 인지할 수 있다.

---

## 예시

아래와 같은 부모 클래스가 있을 때

```java
public class Parent {

    public void greet() {
        System.out.println("Parent.greet");
    }

    public void print(String msg) {
        System.out.println("Parent.print : " + msg);
    }

    public void print(String msg1, String msg2) {
        System.out.println("Parent.print : " + msg1 + " / " + msg2);
    }
}
```

아래처럼 @Override 애너테이션을 붙이지 않을 경우 예상치 못한 오류가 발생할 수 있다.

```java
public class BadChild extends Parent {

    // 메서드명 오타
    public void great() {
        System.out.println("BadChild.great");
    }

    // 파라미터 타입 불일치
    public void print(Object msg) {
        System.out.println("BadChild.print : " + msg);
    }

    // 파라미터 수 불일치
    public void print(String msg1, String msg2, String msg3) {
        System.out.println("BadChild.print : " + msg1 + " / " + msg2 + " / " + msg3);
    }
}
```

컴파일 타임에 잡지 못하는 오류는 나쁜 오류로 이런 실수를 막기 위해서라도 @Override 애너테이션을 붙이는 습관을 들여야 한다. 접근 제어자 범위 축소, 체크 예외 확장 등은 @Override 애너테이션이 없어도 컴파일러가 막는다.

```java
    public static void main(String[] args) {
        Parent p = new BadChild();
        p.greet();
        p.print("hello");
        p.print("hello", "java");
        // Parent.greet
        // Parent.print : hello
        // Parent.print : hello / java

        Parent p2 = new GoodChild();
        p2.greet();
        p2.print("hello");
        p2.print("hello", "java");
        // GoodChild.greet
        // GoodChild.print : hello
        // GoodChild.print : hello / java

    }
```

---
