![image](https://github.com/user-attachments/assets/0013b6f4-5706-4cbb-9a55-9c4a3efe0a9d)


# mobile-sandbox

목표 : Mobsf를 활용한 스파이앱 분석
인원 : 3명
역할 : 팀장(PM) / 동적분석
개발일정 : 2024.05.14~2024.05.27
사용기술 : Mobsf, ARM, Emulator, Frida, IDA, Python
프로젝트 요약 : 경찰청 폴안티스파이 사칭앱
mobSF 정적 및 동적 분석 및 일원화 API 구현
Notion : [Team page](https://heavenly-sponge-d64.notion.site/2-d09c0fa1f5a748569f18d202b69aca0e)
실행영상 : [youtube](https://www.youtube.com/watch?v=sO60AVj6Lf0)
분석 보고서 : [Googlelink](https://drive.google.com/file/d/1bXyxwwoQCoCwd4Ng8dZrNeca1Rh5G6n5/view)


주요 기능 :
정적 분석: 안드로이드 APK, iOS IPA, 그리고 Windows 앱의 소스 코드를 분석하여 보안 취약점을 식별
동적 분석: 앱을 실제로 실행시켜 분석하는 기능, 런타임에서 관찰을 통한 보안문제 식별
앱 프로파일링: 앱의 기본 정보와 사용 권한, 활동, 서비스, 제공자 등을 상세하게 리포트
API 테스트: MobSF를 사용하여 API 테스트하고, 안전하지 않은 API 사용 식별
GitHub 통합: 프로젝트 코드는 GitHub에 공개를 통해 커뮤니티의 기여

개인 성과:
Mobsf 환경 구축 및 에뮬레이터 연동
.dex 파일 IDA분석 후 보안 관련 함수 정보 확인
동적분석 및 frida 우회 스크립트 작성
API 활용 및 함수 사용
문서 작성 및 발표
노션 팀 페이지 제작
