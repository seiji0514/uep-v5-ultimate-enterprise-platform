import type { Meta, StoryObj } from '@storybook/react';
import { EmptyState } from './EmptyState';

const meta: Meta<typeof EmptyState> = {
  component: EmptyState,
  title: 'Common/EmptyState',
};
export default meta;

type Story = StoryObj<typeof EmptyState>;

export const Default: Story = {
  args: { message: 'データがありません' },
};

export const WithSubMessage: Story = {
  args: {
    message: '受注データがありません',
    subMessage: '受注が登録されるとここに表示されます',
  },
};
