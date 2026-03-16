from .schemas import TraceStep


def binary_search_trace(arr: list[int], target: int) -> list[TraceStep]:
    steps: list[TraceStep] = []
    left = 0
    right = len(arr) - 1
    step_num = 1

    while left <= right:
        mid = (left + right) // 2
        steps.append(
            TraceStep(
                step=step_num,
                state=arr.copy(),
                highlight=[left, mid, right],
                code_line=3,
                caption=f"Check middle index {mid} with value {arr[mid]}",
            )
        )
        step_num += 1

        if arr[mid] == target:
            steps.append(
                TraceStep(
                    step=step_num,
                    state=arr.copy(),
                    highlight=[mid],
                    code_line=4,
                    caption=f"Found target {target} at index {mid}",
                )
            )
            return steps
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    steps.append(
        TraceStep(
            step=step_num,
            state=arr.copy(),
            highlight=[],
            code_line=8,
            caption=f"Target {target} not found",
        )
    )
    return steps


def bubble_sort_trace(arr: list[int]) -> list[TraceStep]:
    steps: list[TraceStep] = []
    local = arr.copy()
    step_num = 1

    for i in range(len(local)):
        for j in range(0, len(local) - i - 1):
            steps.append(
                TraceStep(
                    step=step_num,
                    state=local.copy(),
                    highlight=[j, j + 1],
                    code_line=3,
                    caption=f"Compare index {j} and {j + 1}",
                )
            )
            step_num += 1
            if local[j] > local[j + 1]:
                local[j], local[j + 1] = local[j + 1], local[j]
                steps.append(
                    TraceStep(
                        step=step_num,
                        state=local.copy(),
                        highlight=[j, j + 1],
                        code_line=4,
                        caption=f"Swap {j} and {j + 1}",
                    )
                )
                step_num += 1

    steps.append(
        TraceStep(
            step=step_num,
            state=local.copy(),
            highlight=[],
            code_line=5,
            caption="Sorting completed",
        )
    )
    return steps
