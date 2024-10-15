document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('date-form');
    const dateInputs = document.getElementById('dateInputs');

    // 라디오 버튼의 변경 이벤트 리스너 추가
    form.addEventListener('change', (event) => {
        if (event.target.name === 'calendarType') {
            const selectedType = event.target.value;

            // 선택된 달력 유형에 따라 추가 로직 처리
            if (selectedType === 'lunar') {
                console.log("음력 생일이 선택되었습니다.");
                // 음력 관련 로직 (필요시)
            } else {
                console.log("양력 생일이 선택되었습니다.");
                // 양력 관련 로직 (필요시)
            }
        }
    });

    // 폼 제출 처리
    form.addEventListener('submit', (event) => {
        event.preventDefault(); // 기본 제출 동작 방지
        submitForm(); // 제출 함수 호출
    });
});

// 제출 함수
function submitForm() {
    const formData = new FormData(document.getElementById('date-form'));
    const calendarType = formData.get('calendarType');

    if (calendarType === 'solar') {
        // 양력일 경우 solYear, solMonth, solDay 변수로 받기
        const solYear = formData.get('year');
        const solMonth = formData.get('month');
        const solDay = formData.get('day');

        console.log("양력 생일:", { solYear, solMonth, solDay });
        // 양력 생일 처리 로직 추가
    } else {
        // 음력일 경우 입력된 값을 그대로 반환
        const lunarYear = formData.get('year');
        const lunarMonth = formData.get('month');
        const lunarDay = formData.get('day');

        console.log("음력 생일:", { lunarYear, lunarMonth, lunarDay });
        // 음력 생일 처리 로직 추가 (필요시)
    }
}